import Formal.CubicGap.Counts
import Formal.MultilinearGap.PaperFoundations

/-! # Strictly positive boxes of bounded aspect ratio

The gap-ratio class of the positive-box theorem: every finite dimension, every
squarefree support with nonnegative coefficients, and every box
`∏ [l i, u i]` with `0 < l i ≤ u i` and `u i ≤ rho * l i`, evaluated at a point
of the box where the full graph-hull gap is positive.

This file fixes the class (`boxAspectRatios`), its supremum
(`boxAspectSupremum`), and the uniform-bound predicate
(`PositiveBoxAspectBound`); it proves nonemptiness and boundedness *before* any
supremum is compared, reconciles the class with the common-aspect class on
`[1, rho]^n` (`commonAspectBoxRatios`), records the normalization
`x i = 1 + (rho - 1) * p i` together with the vertex value of a physical
monomial, and derives the sandwich `0 ≤ chgap ≤ tbtgap` on a strictly positive
box, hence that every ratio of the class is at least one.

All box semantics (`coordinateBox`, `boxPoint`, `boxGraph`,
`boxEnvelopeValues`, `boxHullGap`, `boxTermwiseGap`) and the comparison
`box_gap_comparison` are reused unchanged from `BoxTransfer`, `Attainment` and
`PaperFoundations`.
-/

namespace MultilinearGap

open CubicGap

noncomputable section

/-- All gap ratios on strictly positive boxes whose coordinate aspect ratios are
at most `rho`: every dimension, support and nonnegative coefficient vector is
allowed, and the point must have a positive full hull gap. -/
def boxAspectRatios (rho : ℝ) : Set ℝ := {r | ∃ (I : Type) (hI : Fintype I)
    (hEq : DecidableEq I),
  letI := hI
  letI := hEq
  ∃ (S : Finset (Finset I)) (a : Finset I → ℝ) (l u x : I → ℝ),
    (∀ s ∈ S, 0 ≤ a s) ∧ (∀ i, 0 < l i) ∧ (∀ i, l i ≤ u i) ∧ (∀ i, u i ≤ rho * l i) ∧
      x ∈ coordinateBox l u ∧ 0 < boxHullGap l u (supportPolynomial S a) x ∧
      r = boxTermwiseGap S a l u x / boxHullGap l u (supportPolynomial S a) x}

/-- The same ratios restricted to the common-aspect boxes `[1, rho]^n`, which is
the class used by the lower-bound source. -/
def commonAspectBoxRatios (rho : ℝ) : Set ℝ := {r | ∃ (I : Type) (hI : Fintype I)
    (hEq : DecidableEq I),
  letI := hI
  letI := hEq
  ∃ (S : Finset (Finset I)) (a : Finset I → ℝ) (x : I → ℝ),
    (∀ s ∈ S, 0 ≤ a s) ∧ x ∈ coordinateBox (fun _ => 1) (fun _ => rho) ∧
      0 < boxHullGap (fun _ => 1) (fun _ => rho) (supportPolynomial S a) x ∧
      r = boxTermwiseGap S a (fun _ => 1) (fun _ => rho) x /
        boxHullGap (fun _ => 1) (fun _ => rho) (supportPolynomial S a) x}

/-- The worst-case ratio `C_box(rho)` on strictly positive boxes of aspect ratio
at most `rho`. Meaningful only together with the nonemptiness and boundedness
results below. -/
def boxAspectSupremum (rho : ℝ) : ℝ := sSup (boxAspectRatios rho)

/-- The worst-case ratio over the common-aspect boxes `[1, rho]^n`. -/
def commonAspectBoxSupremum (rho : ℝ) : ℝ := sSup (commonAspectBoxRatios rho)

/-- A uniform termwise-to-hull bound `U` for all nonnegative squarefree
polynomials on all strictly positive boxes of aspect ratio at most `rho`. -/
def PositiveBoxAspectBound (rho U : ℝ) : Prop :=
  ∀ (I : Type) [Fintype I] [DecidableEq I]
    (S : Finset (Finset I)) (a : Finset I → ℝ) (l u x : I → ℝ),
    (∀ s ∈ S, 0 ≤ a s) → (∀ i, 0 < l i) → (∀ i, l i ≤ u i) → (∀ i, u i ≤ rho * l i) →
      x ∈ coordinateBox l u →
        boxTermwiseGap S a l u x ≤ U * boxHullGap l u (supportPolynomial S a) x

/-! ## The bilinear witness

One bilinear monomial with coefficient one on `[1, rho]^2`, evaluated at the
centre, has a positive hull gap and ratio exactly one. -/

private theorem bilinear_box_polynomial :
    supportPolynomial {(Finset.univ : Finset (Fin 2))} (fun _ => 1) =
      monomial (Finset.univ : Finset (Fin 2)) := by
  funext x
  simp [supportPolynomial]

private theorem bilinear_box_gap_positive {rho : ℝ} (hrho : 1 < rho) :
    0 < boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho)
      (monomial (Finset.univ : Finset (Fin 2))) (fun _ => (1 + rho) / 2) := by
  have hlu : ∀ _ : Fin 2, (1 : ℝ) ≤ rho := fun _ => hrho.le
  have hx : (fun _ => (1 + rho) / 2 : Fin 2 → ℝ) ∈
      coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho) :=
    fun _ => ⟨by linarith, by linarith⟩
  have hf : SeparatelyAffine (monomial (Finset.univ : Finset (Fin 2))) :=
    monomial_coordinate_affine _
  have hend := boxEnvelopeValues_endpoints (fun _ => (1 : ℝ)) (fun _ => rho) hlu
    (monomial (Finset.univ : Finset (Fin 2))) hf _ hx
  have hgraph : monomial (Finset.univ : Finset (Fin 2)) (fun _ => (1 + rho) / 2) ∈
      boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => rho)
        (monomial (Finset.univ : Finset (Fin 2))) (fun _ => (1 + rho) / 2) :=
    subset_convexHull ℝ _ ⟨hx, rfl⟩
  have hml : ((fun _ => (1 : ℝ) : Fin 2 → ℝ), (1 : ℝ)) ∈
      boxGraph (fun _ => (1 : ℝ)) (fun _ => rho)
        (monomial (Finset.univ : Finset (Fin 2))) :=
    ⟨fun _ => ⟨le_rfl, hrho.le⟩, by simp [monomial]⟩
  have hmu : ((fun _ => rho : Fin 2 → ℝ), rho ^ 2) ∈
      boxGraph (fun _ => (1 : ℝ)) (fun _ => rho)
        (monomial (Finset.univ : Finset (Fin 2))) :=
    ⟨fun _ => ⟨hrho.le, le_rfl⟩, by simp [monomial]⟩
  have hmid := convex_convexHull ℝ
    (boxGraph (fun _ => (1 : ℝ)) (fun _ => rho)
      (monomial (Finset.univ : Finset (Fin 2))))
    (subset_convexHull ℝ _ hml) (subset_convexHull ℝ _ hmu)
    (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num)
  have heq : (1 / 2 : ℝ) • ((fun _ => (1 : ℝ) : Fin 2 → ℝ), (1 : ℝ)) +
      (1 / 2 : ℝ) • ((fun _ => rho : Fin 2 → ℝ), rho ^ 2) =
      ((fun _ => (1 + rho) / 2 : Fin 2 → ℝ), (1 + rho ^ 2) / 2) := by
    apply Prod.ext
    · funext i
      change (1 / 2 : ℝ) * 1 + (1 / 2 : ℝ) * rho = (1 + rho) / 2
      ring
    · change (1 / 2 : ℝ) * 1 + (1 / 2 : ℝ) * rho ^ 2 = (1 + rho ^ 2) / 2
      ring
  rw [heq] at hmid
  have hmem : (1 + rho ^ 2) / 2 ∈
      boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => rho)
        (monomial (Finset.univ : Finset (Fin 2))) (fun _ => (1 + rho) / 2) := hmid
  have hsup := hend.2.2 hmem
  have hinf := hend.1.2 hgraph
  have hval : monomial (Finset.univ : Finset (Fin 2)) (fun _ => (1 + rho) / 2) =
      ((1 + rho) / 2) ^ 2 := by
    simp [monomial, div_pow]
  rw [hval] at hinf
  rw [boxHullGap]
  nlinarith [hsup, hinf, mul_pos (sub_pos.mpr hrho) (sub_pos.mpr hrho)]

/-- The data of the bilinear witness on `[1, rho]^2`: it lies in the box, its
hull gap is positive, and its termwise-to-hull ratio is exactly one. -/
private theorem bilinear_box_witness {rho : ℝ} (hrho : 1 < rho) :
    (fun _ => (1 + rho) / 2 : Fin 2 → ℝ) ∈
        coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho) ∧
      0 < boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho)
        (supportPolynomial {(Finset.univ : Finset (Fin 2))} (fun _ => 1))
        (fun _ => (1 + rho) / 2) ∧
      (1 : ℝ) = boxTermwiseGap {(Finset.univ : Finset (Fin 2))} (fun _ => 1)
          (fun _ => (1 : ℝ)) (fun _ => rho) (fun _ => (1 + rho) / 2) /
        boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho)
          (supportPolynomial {(Finset.univ : Finset (Fin 2))} (fun _ => 1))
          (fun _ => (1 + rho) / 2) := by
  have hg := bilinear_box_gap_positive hrho
  refine ⟨fun _ => ⟨by linarith, by linarith⟩, ?_, ?_⟩
  · simpa only [bilinear_box_polynomial] using hg
  · simp only [boxTermwiseGap, bilinear_box_polynomial, Finset.sum_singleton, one_mul]
    exact (div_self hg.ne').symm

/-! ## PB01: nonemptiness, boundedness and monotonicity -/

/-- One bilinear monomial on `[1, rho]^2` realizes the ratio one. -/
theorem one_mem_boxAspectRatios {rho : ℝ} (hrho : 1 < rho) : (1 : ℝ) ∈ boxAspectRatios rho := by
  obtain ⟨hx, hpos, hratio⟩ := bilinear_box_witness hrho
  exact ⟨Fin 2, inferInstance, inferInstance, {Finset.univ}, fun _ => 1,
    fun _ => 1, fun _ => rho, fun _ => (1 + rho) / 2, by simp, fun _ => one_pos,
    fun _ => hrho.le, fun _ => by simp, hx, hpos, hratio⟩

/-- The class is nonempty for every admissible aspect bound. -/
theorem boxAspectRatios_nonempty {rho : ℝ} (hrho : 1 < rho) :
    (boxAspectRatios rho).Nonempty := ⟨1, one_mem_boxAspectRatios hrho⟩

/-- A uniform positive-box bound bounds every ratio of the class. -/
theorem boxAspectRatios_le {rho U : ℝ} (hU : PositiveBoxAspectBound rho U)
    {r : ℝ} (hr : r ∈ boxAspectRatios rho) : r ≤ U := by
  obtain ⟨I, hI, hEq, S, a, l, u, x, ha, hl, hlu, hasp, hx, hpos, rfl⟩ := hr
  let _ := hI
  let _ := hEq
  exact (div_le_iff₀ hpos).mpr (hU I S a l u x ha hl hlu hasp hx)

/-- The class is bounded above by any uniform positive-box bound. -/
theorem boxAspectRatios_bddAbove {rho U : ℝ} (hU : PositiveBoxAspectBound rho U) :
    BddAbove (boxAspectRatios rho) := ⟨U, fun _ hr => boxAspectRatios_le hU hr⟩

/-- Enlarging the aspect bound enlarges the class: strict positivity of `l`
turns `u i ≤ rho * l i` into `u i ≤ rho' * l i`. -/
theorem boxAspectRatios_subset {rho rho' : ℝ} (h : rho ≤ rho') :
    boxAspectRatios rho ⊆ boxAspectRatios rho' := by
  rintro r ⟨I, hI, hEq, S, a, l, u, x, ha, hl, hlu, hasp, hx, hpos, hr⟩
  exact ⟨I, hI, hEq, S, a, l, u, x, ha, hl, hlu,
    fun i => (hasp i).trans (mul_le_mul_of_nonneg_right h (hl i).le), hx, hpos, hr⟩

theorem boxAspectRatios_mono : Monotone boxAspectRatios :=
  fun _ _ h => boxAspectRatios_subset h

/-- Monotonicity of `C_box`, stated with the boundedness the supremum needs. -/
theorem boxAspectSupremum_mono {rho rho' U : ℝ} (hrho : 1 < rho) (h : rho ≤ rho')
    (hU : PositiveBoxAspectBound rho' U) :
    boxAspectSupremum rho ≤ boxAspectSupremum rho' :=
  csSup_le_csSup (boxAspectRatios_bddAbove hU) (boxAspectRatios_nonempty hrho)
    (boxAspectRatios_subset h)

/-- Any uniform positive-box bound bounds the supremum. -/
theorem boxAspectSupremum_le {rho U : ℝ} (hrho : 1 < rho)
    (hU : PositiveBoxAspectBound rho U) : boxAspectSupremum rho ≤ U :=
  csSup_le (boxAspectRatios_nonempty hrho) (fun _ hr => boxAspectRatios_le hU hr)

/-! ## PB02: reconciling the two source classes -/

/-- Every common-aspect ratio on `[1, rho]^n` is a ratio of the general
strictly positive class, so lower bounds proved on `[1, rho]^n` transfer. -/
theorem commonAspectBoxRatios_subset_boxAspectRatios {rho : ℝ} (hrho : 1 ≤ rho) :
    commonAspectBoxRatios rho ⊆ boxAspectRatios rho := by
  rintro r ⟨I, hI, hEq, S, a, x, ha, hx, hpos, hr⟩
  exact ⟨I, hI, hEq, S, a, fun _ => 1, fun _ => rho, x, ha, fun _ => one_pos,
    fun _ => hrho, fun _ => by simp, hx, hpos, hr⟩

/-- The bilinear witness already lives on `[1, rho]^2`. -/
theorem one_mem_commonAspectBoxRatios {rho : ℝ} (hrho : 1 < rho) :
    (1 : ℝ) ∈ commonAspectBoxRatios rho := by
  obtain ⟨hx, hpos, hratio⟩ := bilinear_box_witness hrho
  exact ⟨Fin 2, inferInstance, inferInstance, {Finset.univ}, fun _ => 1,
    fun _ => (1 + rho) / 2, by simp, hx, hpos, hratio⟩

theorem commonAspectBoxRatios_nonempty {rho : ℝ} (hrho : 1 < rho) :
    (commonAspectBoxRatios rho).Nonempty := ⟨1, one_mem_commonAspectBoxRatios hrho⟩

/-- A single common-aspect ratio is a lower bound for `C_box(rho)`: the form in
which a `[1, rho]^n` construction bounds the general supremum from below. -/
theorem le_boxAspectSupremum_of_mem_commonAspect {rho U r : ℝ} (hrho : 1 ≤ rho)
    (hU : PositiveBoxAspectBound rho U) (hr : r ∈ commonAspectBoxRatios rho) :
    r ≤ boxAspectSupremum rho :=
  le_csSup (boxAspectRatios_bddAbove hU)
    (commonAspectBoxRatios_subset_boxAspectRatios hrho hr)

/-- The common-aspect supremum never exceeds the general one. -/
theorem commonAspectBoxSupremum_le_boxAspectSupremum {rho U : ℝ} (hrho : 1 < rho)
    (hU : PositiveBoxAspectBound rho U) :
    commonAspectBoxSupremum rho ≤ boxAspectSupremum rho :=
  csSup_le_csSup (boxAspectRatios_bddAbove hU) (commonAspectBoxRatios_nonempty hrho)
    (commonAspectBoxRatios_subset_boxAspectRatios hrho.le)

/-! ## PB03: the normalization `x i = 1 + (rho - 1) * p i` -/

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] [DecidableEq I] in
/-- The normalization is exactly the affine parameterization `boxPoint` of the
common-aspect box `[1, rho]^n`. -/
theorem boxPoint_common_aspect (rho : ℝ) (p : I → ℝ) (i : I) :
    boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p i = 1 + (rho - 1) * p i := rfl

omit [Fintype I] [DecidableEq I] in
/-- The normalization maps the unit cube onto `[1, rho]^n`. -/
theorem boxPoint_image_cube (rho : ℝ) (hrho : 1 ≤ rho) :
    boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) '' cube I =
      coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho) := by
  ext x
  constructor
  · rintro ⟨p, hp, rfl⟩
    exact boxPoint_mem _ _ p (fun _ => hrho) hp
  · intro hx
    exact exists_boxPoint _ _ (fun _ => hrho) x hx

/-- The number of successful coordinates of a vertex inside a support: the
restriction of `CubicGap.count` to `s`, given as a `Finset.filter` cardinality. -/
def boxSuccessCount (s : Finset I) (v : Vertex I) : ℕ :=
  (s.filter fun i => v i = true).card

omit [DecidableEq I] in
/-- On the full support the success count is the ambient `CubicGap.count`. -/
theorem boxSuccessCount_univ (v : Vertex I) :
    boxSuccessCount (Finset.univ : Finset I) v = count v := rfl

omit [Fintype I] [DecidableEq I] in
/-- At a vertex of the normalization the physical monomial `∏ i ∈ s, x i` is
`(1 + (rho - 1)) ^ K` with `K` the number of successes of the vertex in `s`. -/
theorem monomial_boxPoint_vertex (rho : ℝ) (s : Finset I) (v : Vertex I) :
    monomial s (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v)) =
      (1 + (rho - 1)) ^ boxSuccessCount s v := by
  have hterm : ∀ i ∈ s,
      boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v) i =
        if v i = true then 1 + (rho - 1) else 1 := by
    intro i _
    by_cases hv : v i = true <;> simp [boxPoint, vertexPoint, hv]
  rw [monomial, Finset.prod_congr rfl hterm, Finset.prod_ite, Finset.prod_const,
    Finset.prod_const_one, mul_one]
  rfl

omit [Fintype I] [DecidableEq I] in
/-- The same vertex value written with the aspect ratio itself. -/
theorem monomial_boxPoint_vertex_pow (rho : ℝ) (s : Finset I) (v : Vertex I) :
    monomial s (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v)) =
      rho ^ boxSuccessCount s v := by
  rw [monomial_boxPoint_vertex]
  norm_num

/-! ## PB04: the sandwich and the lower bound one for every ratio -/

omit [Fintype I] [DecidableEq I] in
/-- On a strictly positive box every point is strictly positive, the full
graph-hull gap is nonnegative, and it never exceeds the termwise relaxation.
The last two conclusions are `box_gap_comparison`, which needs only `l ≤ u`. -/
theorem positiveBox_gap_sandwich [Finite I] (S : Finset (Finset I)) (a : Finset I → ℝ)
    (ha : ∀ s ∈ S, 0 ≤ a s) (l u x : I → ℝ) (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i)
    (hx : x ∈ coordinateBox l u) :
    (∀ i, 0 < x i) ∧ 0 ≤ boxHullGap l u (supportPolynomial S a) x ∧
      boxHullGap l u (supportPolynomial S a) x ≤ boxTermwiseGap S a l u x :=
  ⟨fun i => lt_of_lt_of_le (hl i) (hx i).1,
    (box_gap_comparison S a ha l u x hlu hx).1,
    (box_gap_comparison S a ha l u x hlu hx).2⟩

/-- Every ratio of the strictly positive aspect class is at least one. -/
theorem one_le_of_mem_boxAspectRatios {rho r : ℝ} (hr : r ∈ boxAspectRatios rho) :
    1 ≤ r := by
  obtain ⟨I, hI, hEq, S, a, l, u, x, ha, hl, hlu, hasp, hx, hpos, rfl⟩ := hr
  let _ := hI
  let _ := hEq
  exact (one_le_div hpos).mpr (positiveBox_gap_sandwich S a ha l u x hl hlu hx).2.2

/-- Hence `1 ≤ C_box(rho)` whenever the supremum is meaningful. -/
theorem one_le_boxAspectSupremum {rho U : ℝ} (hrho : 1 < rho)
    (hU : PositiveBoxAspectBound rho U) : 1 ≤ boxAspectSupremum rho :=
  le_csSup (boxAspectRatios_bddAbove hU) (one_mem_boxAspectRatios hrho)

end
end MultilinearGap
