import Formal.MultilinearGap.PositiveBox

/-! # Transfer from `[1, rho]^n` to an unequal strictly positive box

This file discharges PB23 and PB24 of the positive-box package
(`formal/topics/18-positive-box/CLAIMS.md`).

**PB23.** For `rho > 1` and a box with `0 < l i ≤ u i ≤ rho * l i`, put
`s i = (u i / l i - 1) / (rho - 1)` (`originalBoxShare`) and
`z i = l i * ((1 - s i) + s i * x i)` (`originalBoxPoint`).  The share lies in
`[0, 1]`, and in `(0, 1]` exactly at the non-fixed coordinates
(`originalBoxShare_eq_zero_iff`).  The map is an affine bijection from
`[1, rho]^n` onto `∏ [l i, u i]` with the explicit two-sided inverse
`originalBoxInverse`, **provided every coordinate is non-fixed**
(`originalBox_invOn`, `originalBox_bijOn`); with fixed coordinates allowed it is
still surjective (`exists_originalBoxPoint`), which is all the gap transfer
needs.  Each original monomial expands into a multilinear polynomial in the
`[1, rho]` variables with nonnegative coefficients
(`monomial_originalBox_expansion`, `originalExpansionCoefficient_nonneg`).

**PB24.** The full graph-hull gap is invariant under the transfer map
(`boxHullGap_originalBoxPoint`, `boxHullGap_originalBox_expansion`), and the
termwise gap on the original box is at most the termwise gap of the expansion on
`[1, rho]^n` (`boxTermwiseGap_originalBox_le_expansion`).  The second inequality
is obtained from the envelope statement the source names: on any coordinate box
the concave envelope of a sum is at most the sum of the concave envelopes
(`boxEnvelope_sSup_sum_le`) and the convex envelope of a sum is at least the sum
of the convex envelopes (`boxEnvelope_sum_le_sInf`), hence `boxHullGap_sum_le`.

The last section records the resulting transfer step: any uniform
termwise-to-hull bound on the common-aspect boxes `[1, rho]^n` is a
`PositiveBoxAspectBound`.  The common-aspect bound itself (PB22) is *not* proved
here.

All box semantics and the affine-rescaling machinery (`coordinateBox`,
`boxPoint`, `boxHullGap`, `boxTermwiseGap`, `boxEnvelopeValues_eq_of_mem`,
`boxHullGap_eq_of_mem`, `exists_boxPoint`, `boxPoint_mem`,
`boxExpansionCoefficient`, `monomial_box_expansion`,
`supportPolynomial_box_expansion`, `boxPolynomialExpansion_sum`,
`boxHullGap_monomial_scale`, `separatelyAffine_box_monomial`) are reused
unchanged from `BoxTransfer`, `GeneralGaps` and `PaperFoundations`.
-/

namespace MultilinearGap

open CubicGap

noncomputable section

/-! ## PB23: the affine transfer map and its inverse -/

section Transfer

variable {I : Type*}

/-- The share `s i = (u i / l i - 1) / (rho - 1)` of the full aspect ratio
`rho` used by coordinate `i`. -/
def originalBoxShare (rho : ℝ) (l u : I → ℝ) (i : I) : ℝ :=
  (u i / l i - 1) / (rho - 1)

/-- The transfer map `z i = l i * ((1 - s i) + s i * x i)` from the
common-aspect box `[1, rho]^n` to the original box `∏ [l i, u i]`. -/
def originalBoxPoint (rho : ℝ) (l u x : I → ℝ) : I → ℝ :=
  fun i => l i * ((1 - originalBoxShare rho l u i) + originalBoxShare rho l u i * x i)

/-- The value `l i * (1 - s i)` of the transfer map at `x i = 0`: the constant
term of the affine map whose value at `x i = 1` is `l i`. -/
def originalBoxIntercept (rho : ℝ) (l u : I → ℝ) : I → ℝ :=
  fun i => l i * (1 - originalBoxShare rho l u i)

/-- The candidate inverse `x i = 1 + (rho - 1) * (z i - l i) / (u i - l i)`. -/
def originalBoxInverse (rho : ℝ) (l u z : I → ℝ) : I → ℝ :=
  fun i => 1 + (rho - 1) * ((z i - l i) / (u i - l i))

/-- The share is nonnegative on every box with `l ≤ u`. -/
theorem originalBoxShare_nonneg {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (i : I) :
    0 ≤ originalBoxShare rho l u i := by
  have h1 : (1 : ℝ) ≤ u i / l i := (le_div_iff₀ (hl i)).mpr (by rw [one_mul]; exact hlu i)
  exact div_nonneg (by linarith) (by linarith)

/-- The share is at most one exactly because `rho` bounds the aspect ratio. -/
theorem originalBoxShare_le_one {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hasp : ∀ i, u i ≤ rho * l i) (i : I) :
    originalBoxShare rho l u i ≤ 1 := by
  have h : u i / l i ≤ rho :=
    (div_le_iff₀ (hl i)).mpr (hasp i)
  rw [originalBoxShare, div_le_one (by linarith)]
  linarith

/-- The share vanishes exactly at a fixed coordinate. -/
theorem originalBoxShare_eq_zero_iff {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (i : I) :
    originalBoxShare rho l u i = 0 ↔ l i = u i := by
  have hr : rho - 1 ≠ 0 := sub_ne_zero.mpr hrho.ne'
  rw [originalBoxShare, div_eq_zero_iff]
  constructor
  · rintro (h | h)
    · have h1 : u i / l i = 1 := by linarith
      have h2 := (div_eq_iff (hl i).ne').mp h1
      linarith
    · exact absurd h hr
  · intro h
    exact Or.inl (by rw [← h, div_self (hl i).ne', sub_self])

/-- The share is strictly positive at a non-fixed coordinate. -/
theorem originalBoxShare_pos {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) {i : I} (hlt : l i < u i) :
    0 < originalBoxShare rho l u i := by
  have h : 1 < u i / l i := (one_lt_div (hl i)).mpr hlt
  exact div_pos (by linarith) (by linarith)

/-- PB23, the share range on a box that may still contain fixed coordinates. -/
theorem originalBoxShare_mem_Icc {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (hasp : ∀ i, u i ≤ rho * l i) (i : I) :
    originalBoxShare rho l u i ∈ Set.Icc (0 : ℝ) 1 :=
  ⟨originalBoxShare_nonneg hrho hl hlu i, originalBoxShare_le_one hrho hl hasp i⟩

/-- PB23, the share range as stated in the source: `s i ∈ (0, 1]` once the
fixed coordinates have been removed. -/
theorem originalBoxShare_mem_Ioc {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hasp : ∀ i, u i ≤ rho * l i) {i : I} (hlt : l i < u i) :
    originalBoxShare rho l u i ∈ Set.Ioc (0 : ℝ) 1 :=
  ⟨originalBoxShare_pos hrho hl hlt, originalBoxShare_le_one hrho hl hasp i⟩

/-- The intercept is nonnegative, since `0 ≤ s i ≤ 1` and `0 < l i`. -/
theorem originalBoxIntercept_nonneg {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hasp : ∀ i, u i ≤ rho * l i) (i : I) :
    0 ≤ originalBoxIntercept rho l u i := by
  change 0 ≤ l i * (1 - originalBoxShare rho l u i)
  nlinarith [originalBoxShare_le_one hrho hl hasp i, (hl i).le]

/-- The intercept never exceeds `l i`, the value of the transfer map at
`x i = 1`. -/
theorem originalBoxIntercept_le {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (i : I) :
    originalBoxIntercept rho l u i ≤ l i := by
  change l i * (1 - originalBoxShare rho l u i) ≤ l i
  nlinarith [originalBoxShare_nonneg hrho hl hlu i, (hl i).le]

/-- The transfer map is the affine box parameterization `boxPoint l u`
precomposed with the rescaling of `[1, rho]` onto `[0, 1]`. -/
theorem originalBoxPoint_eq_boxPoint {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (x : I → ℝ) :
    originalBoxPoint rho l u x = boxPoint l u (fun i => (x i - 1) / (rho - 1)) := by
  funext i
  have hr : rho - 1 ≠ 0 := sub_ne_zero.mpr hrho.ne'
  have hli : l i ≠ 0 := (hl i).ne'
  change l i * ((1 - originalBoxShare rho l u i) + originalBoxShare rho l u i * x i) =
    l i + (u i - l i) * ((x i - 1) / (rho - 1))
  simp only [originalBoxShare]
  field_simp
  ring

/-- The transfer map is also the affine map with intercept
`originalBoxIntercept` at `x i = 0` and value `l i` at `x i = 1`.  This is the
form in which `monomial_box_expansion` applies directly in the `[1, rho]`
variables. -/
theorem originalBoxPoint_eq_boxPoint_intercept (rho : ℝ) (l u x : I → ℝ) :
    originalBoxPoint rho l u x = boxPoint (originalBoxIntercept rho l u) l x := by
  funext i
  change l i * ((1 - originalBoxShare rho l u i) + originalBoxShare rho l u i * x i) =
    l i * (1 - originalBoxShare rho l u i) +
      (l i - l i * (1 - originalBoxShare rho l u i)) * x i
  ring

/-- The transfer map intertwines the two affine parameterizations: it carries
the `[1, rho]^n` parameterization of a cube point `p` to the `∏ [l i, u i]`
parameterization of the same `p`. -/
theorem originalBoxPoint_commonAspect {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (p : I → ℝ) :
    originalBoxPoint rho l u (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) =
      boxPoint l u p := by
  funext i
  have hr : rho - 1 ≠ 0 := sub_ne_zero.mpr hrho.ne'
  have hli : l i ≠ 0 := (hl i).ne'
  change l i * ((1 - originalBoxShare rho l u i) +
      originalBoxShare rho l u i * (1 + (rho - 1) * p i)) = l i + (u i - l i) * p i
  simp only [originalBoxShare]
  field_simp
  ring

/-- The transfer map sends `[1, rho]^n` into the original box. -/
theorem originalBoxPoint_mem {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) {x : I → ℝ}
    (hx : x ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) :
    originalBoxPoint rho l u x ∈ coordinateBox l u := by
  rw [originalBoxPoint_eq_boxPoint hrho hl]
  refine boxPoint_mem l u _ hlu fun i => ?_
  have h1 : (1 : ℝ) ≤ x i := (hx i).1
  have h2 : x i ≤ rho := (hx i).2
  have hr : (0 : ℝ) < rho - 1 := by linarith
  exact ⟨div_nonneg (by linarith) hr.le, (div_le_one hr).mpr (by linarith)⟩

/-- The candidate inverse sends the original box into `[1, rho]^n`; this needs
every coordinate to be non-fixed. -/
theorem originalBoxInverse_mem {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hne : ∀ i, l i < u i) {z : I → ℝ} (hz : z ∈ coordinateBox l u) :
    originalBoxInverse rho l u z ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho) := by
  intro i
  have hd : (0 : ℝ) < u i - l i := sub_pos.mpr (hne i)
  have h0 : 0 ≤ (z i - l i) / (u i - l i) := div_nonneg (by linarith [(hz i).1]) hd.le
  have h1 : (z i - l i) / (u i - l i) ≤ 1 := (div_le_one hd).mpr (by linarith [(hz i).2])
  refine ⟨?_, ?_⟩
  · change (1 : ℝ) ≤ 1 + (rho - 1) * ((z i - l i) / (u i - l i))
    nlinarith
  · change (1 : ℝ) + (rho - 1) * ((z i - l i) / (u i - l i)) ≤ rho
    nlinarith

/-- `originalBoxInverse` is a left inverse of the transfer map at every
non-fixed box. -/
theorem originalBoxInverse_originalBoxPoint {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hne : ∀ i, l i < u i) (x : I → ℝ) :
    originalBoxInverse rho l u (originalBoxPoint rho l u x) = x := by
  funext i
  have hr : rho - 1 ≠ 0 := sub_ne_zero.mpr hrho.ne'
  have hd : u i - l i ≠ 0 := sub_ne_zero.mpr (hne i).ne'
  rw [originalBoxPoint_eq_boxPoint hrho hl]
  change (1 : ℝ) + (rho - 1) *
    ((l i + (u i - l i) * ((x i - 1) / (rho - 1)) - l i) / (u i - l i)) = x i
  field_simp
  ring

/-- `originalBoxInverse` is a right inverse of the transfer map at every
non-fixed box. -/
theorem originalBoxPoint_originalBoxInverse {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hne : ∀ i, l i < u i) (z : I → ℝ) :
    originalBoxPoint rho l u (originalBoxInverse rho l u z) = z := by
  funext i
  have hr : rho - 1 ≠ 0 := sub_ne_zero.mpr hrho.ne'
  have hd : u i - l i ≠ 0 := sub_ne_zero.mpr (hne i).ne'
  rw [originalBoxPoint_eq_boxPoint hrho hl]
  change l i + (u i - l i) *
    ((1 + (rho - 1) * ((z i - l i) / (u i - l i)) - 1) / (rho - 1)) = z i
  field_simp
  ring

/-- PB23, the explicit two-sided inverse on the two boxes. -/
theorem originalBox_invOn {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hne : ∀ i, l i < u i) :
    Set.InvOn (originalBoxInverse rho l u) (originalBoxPoint rho l u)
      (coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) (coordinateBox l u) :=
  ⟨fun x _ => originalBoxInverse_originalBoxPoint hrho hl hne x,
    fun z _ => originalBoxPoint_originalBoxInverse hrho hl hne z⟩

/-- PB23, the affine bijection `[1, rho]^n → ∏ [l i, u i]`, proved from the
explicit inverse.  Fixed coordinates are excluded: at `l i = u i` the map is not
injective. -/
theorem originalBox_bijOn {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hne : ∀ i, l i < u i) :
    Set.BijOn (originalBoxPoint rho l u)
      (coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) (coordinateBox l u) :=
  (originalBox_invOn hrho hl hne).bijOn
    (fun _ hx => originalBoxPoint_mem hrho hl (fun i => (hne i).le) hx)
    (fun _ hz => originalBoxInverse_mem hrho hne hz)

/-- Surjectivity needs no non-fixed hypothesis: every point of the original box,
including one with fixed coordinates, is the image of a point of `[1, rho]^n`. -/
theorem exists_originalBoxPoint {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) {z : I → ℝ} (hz : z ∈ coordinateBox l u) :
    ∃ x ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho),
      originalBoxPoint rho l u x = z := by
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu z hz
  exact ⟨boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p,
    boxPoint_mem _ _ p (fun _ => hrho.le) hp, originalBoxPoint_commonAspect hrho hl p⟩

/-- The surjectivity of the transfer map, in `Set.SurjOn` form. -/
theorem originalBox_surjOn {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) :
    Set.SurjOn (originalBoxPoint rho l u)
      (coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) (coordinateBox l u) := by
  intro z hz
  obtain ⟨x, hx, hxz⟩ := exists_originalBoxPoint hrho hl hlu hz
  exact ⟨x, hx, hxz⟩

end Transfer

/-! ## PB23: the positive expansion of an original monomial -/

section Expansion

variable {I : Type*} [DecidableEq I]

/-- The coefficient of the squarefree subterm `t ⊆ s` in the expansion of the
original monomial `∏ i ∈ s, z i` in the `[1, rho]` variables. -/
def originalExpansionCoefficient (rho : ℝ) (l u : I → ℝ) (s t : Finset I) : ℝ :=
  (∏ i ∈ t, l i * originalBoxShare rho l u i) *
    ∏ i ∈ s \ t, l i * (1 - originalBoxShare rho l u i)

/-- The expansion coefficient is the generic affine expansion coefficient of the
affine map `originalBoxPoint`. -/
theorem originalExpansionCoefficient_eq (rho : ℝ) (l u : I → ℝ) (s t : Finset I) :
    originalExpansionCoefficient rho l u s t =
      boxExpansionCoefficient (originalBoxIntercept rho l u) l s t := by
  unfold originalExpansionCoefficient boxExpansionCoefficient originalBoxIntercept
  congr 1
  exact Finset.prod_congr rfl fun i _ => by ring

/-- PB23: an original monomial becomes, under the transfer map, a multilinear
polynomial in the `[1, rho]` variables supported on the subsets of `s`. -/
theorem monomial_originalBox_expansion (rho : ℝ) (l u x : I → ℝ) (s : Finset I) :
    monomial s (originalBoxPoint rho l u x) =
      supportPolynomial s.powerset (originalExpansionCoefficient rho l u s) x := by
  have hc : originalExpansionCoefficient rho l u s =
      boxExpansionCoefficient (originalBoxIntercept rho l u) l s := by
    funext t
    exact originalExpansionCoefficient_eq rho l u s t
  rw [originalBoxPoint_eq_boxPoint_intercept, monomial_box_expansion, hc]

/-- PB23: the expansion coefficients are nonnegative. -/
theorem originalExpansionCoefficient_nonneg {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (hasp : ∀ i, u i ≤ rho * l i)
    (s t : Finset I) : 0 ≤ originalExpansionCoefficient rho l u s t := by
  rw [originalExpansionCoefficient_eq]
  exact boxExpansionCoefficient_nonneg _ _ (originalBoxIntercept_nonneg hrho hl hasp)
    (originalBoxIntercept_le hrho hl hlu) s t

/-- The collected coefficient of the expansion of a whole nonnegative
polynomial in the `[1, rho]` variables. -/
def originalPolynomialCoefficient (rho : ℝ) (l u : I → ℝ) (S : Finset (Finset I))
    (a : Finset I → ℝ) (t : Finset I) : ℝ :=
  boxPolynomialCoefficient S a (originalBoxIntercept rho l u) l t

/-- The expansion of a whole polynomial agrees with the transferred original. -/
theorem supportPolynomial_originalBox_expansion (rho : ℝ) (l u x : I → ℝ)
    (S : Finset (Finset I)) (a : Finset I → ℝ) :
    supportPolynomial S a (originalBoxPoint rho l u x) =
      supportPolynomial (boxExpansionSupports S)
        (originalPolynomialCoefficient rho l u S a) x := by
  rw [originalBoxPoint_eq_boxPoint_intercept, supportPolynomial_box_expansion]
  rfl

/-- The collected expansion coefficients are nonnegative. -/
theorem originalPolynomialCoefficient_nonneg {rho : ℝ} (hrho : 1 < rho)
    (S : Finset (Finset I)) (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (hasp : ∀ i, u i ≤ rho * l i)
    (t : Finset I) : 0 ≤ originalPolynomialCoefficient rho l u S a t :=
  boxPolynomialCoefficient_nonneg S a ha _ _ (originalBoxIntercept_nonneg hrho hl hasp)
    (originalBoxIntercept_le hrho hl hlu) t

end Expansion

/-! ## Envelopes of a sum on a coordinate box

The statement the source uses to compare the two termwise gaps: on a box, the
concave envelope of a sum is at most the sum of the concave envelopes, and the
convex envelope of a sum is at least the sum of the convex envelopes. -/

section Envelopes

variable {I J : Type*} [Finite I] [DecidableEq I]

private theorem csSup_envelopeValues_sum_le (S : Finset J) (g : J → (I → ℝ) → ℝ)
    (hg : ∀ j ∈ S, SeparatelyAffine (g j)) (p : I → ℝ) (hp : p ∈ cube I) :
    sSup (envelopeValues (fun q => ∑ j ∈ S, g j q) p) ≤
      ∑ j ∈ S, sSup (envelopeValues (g j) p) := by
  let _ := Fintype.ofFinite I
  refine csSup_le (envelopeValues_nonempty _ p hp) fun z hz => ?_
  obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff _ (separatelyAffine_sum S g hg) p z).mp hz
  have hexpect : μ.expect (fun v => ∑ j ∈ S, g j (vertexPoint v)) =
      ∑ j ∈ S, μ.expect (fun v => g j (vertexPoint v)) := by
    simp only [Law.expect, Finset.mul_sum]
    exact Finset.sum_comm
  rw [← hv, hexpect]
  exact Finset.sum_le_sum fun j hj =>
    le_csSup (envelopeValues_isCompact (g j) (hg j hj) p).bddAbove
      ((mem_cubeGraph_hull_iff _ (hg j hj) p _).mpr ⟨μ, hm, rfl⟩)

private theorem le_csInf_envelopeValues_sum (S : Finset J) (g : J → (I → ℝ) → ℝ)
    (hg : ∀ j ∈ S, SeparatelyAffine (g j)) (p : I → ℝ) (hp : p ∈ cube I) :
    (∑ j ∈ S, sInf (envelopeValues (g j) p)) ≤
      sInf (envelopeValues (fun q => ∑ j ∈ S, g j q) p) := by
  let _ := Fintype.ofFinite I
  refine le_csInf (envelopeValues_nonempty _ p hp) fun z hz => ?_
  obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff _ (separatelyAffine_sum S g hg) p z).mp hz
  have hexpect : μ.expect (fun v => ∑ j ∈ S, g j (vertexPoint v)) =
      ∑ j ∈ S, μ.expect (fun v => g j (vertexPoint v)) := by
    simp only [Law.expect, Finset.mul_sum]
    exact Finset.sum_comm
  rw [← hv, hexpect]
  exact Finset.sum_le_sum fun j hj =>
    csInf_le (envelopeValues_isCompact (g j) (hg j hj) p).bddBelow
      ((mem_cubeGraph_hull_iff _ (hg j hj) p _).mpr ⟨μ, hm, rfl⟩)

/-- The concave envelope of a sum is at most the sum of the concave envelopes,
on any coordinate box. -/
theorem boxEnvelope_sSup_sum_le (S : Finset J) (f : J → (I → ℝ) → ℝ)
    (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (hf : ∀ j ∈ S, SeparatelyAffine (fun q => f j (boxPoint l u q)))
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    sSup (boxEnvelopeValues l u (fun y => ∑ j ∈ S, f j y) x) ≤
      ∑ j ∈ S, sSup (boxEnvelopeValues l u (f j) x) := by
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  rw [boxEnvelopeValues_eq_of_mem l u hlu _ p hp]
  refine (csSup_envelopeValues_sum_le S (fun j q => f j (boxPoint l u q)) hf p hp).trans_eq ?_
  exact Finset.sum_congr rfl fun j _ => by
    rw [boxEnvelopeValues_eq_of_mem l u hlu (f j) p hp]

/-- The convex envelope of a sum is at least the sum of the convex envelopes,
on any coordinate box. -/
theorem boxEnvelope_sum_le_sInf (S : Finset J) (f : J → (I → ℝ) → ℝ)
    (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (hf : ∀ j ∈ S, SeparatelyAffine (fun q => f j (boxPoint l u q)))
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    (∑ j ∈ S, sInf (boxEnvelopeValues l u (f j) x)) ≤
      sInf (boxEnvelopeValues l u (fun y => ∑ j ∈ S, f j y) x) := by
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  rw [boxEnvelopeValues_eq_of_mem l u hlu _ p hp]
  refine Eq.trans_le ?_
    (le_csInf_envelopeValues_sum S (fun j q => f j (boxPoint l u q)) hf p hp)
  exact Finset.sum_congr rfl fun j _ => by
    rw [boxEnvelopeValues_eq_of_mem l u hlu (f j) p hp]

/-- Hence the box graph-hull gap of a sum is at most the sum of the gaps: the
concave envelope shrinks and the convex envelope grows. -/
theorem boxHullGap_sum_le (S : Finset J) (f : J → (I → ℝ) → ℝ)
    (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (hf : ∀ j ∈ S, SeparatelyAffine (fun q => f j (boxPoint l u q)))
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    boxHullGap l u (fun y => ∑ j ∈ S, f j y) x ≤ ∑ j ∈ S, boxHullGap l u (f j) x := by
  have hsup := boxEnvelope_sSup_sum_le S f l u hlu hf x hx
  have hinf := boxEnvelope_sum_le_sInf S f l u hlu hf x hx
  simp only [boxHullGap, Finset.sum_sub_distrib]
  linarith

end Envelopes

/-! ## PB24: what transfers -/

section Gaps

variable {I : Type*} [Finite I] [DecidableEq I]

omit [Finite I] in
/-- A scaled rescaled monomial is separately affine in the box parameter. -/
private theorem separatelyAffine_const_mul_box_monomial (l u : I → ℝ) (c : ℝ)
    (t : Finset I) : SeparatelyAffine (fun q => c * monomial t (boxPoint l u q)) := by
  intro y i r
  have he := separatelyAffine_box_monomial l u t y i r
  simp only at he ⊢
  rw [he]
  ring

omit [DecidableEq I] in
/-- PB24: the full graph-hull gap is invariant under the transfer map.  No
structure of `f` is used; only that the two affine parameterizations agree. -/
theorem boxHullGap_originalBoxPoint {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (f : (I → ℝ) → ℝ) {x : I → ℝ}
    (hx : x ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) :
    boxHullGap l u f (originalBoxPoint rho l u x) =
      boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho)
        (fun y => f (originalBoxPoint rho l u y)) x := by
  classical
  let _ := Fintype.ofFinite I
  obtain ⟨p, hp, rfl⟩ :=
    exists_boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (fun _ => hrho.le) x hx
  have hcomm := originalBoxPoint_commonAspect hrho hl (l := l) (u := u)
  rw [hcomm p, boxHullGap_eq_of_mem l u hlu f p hp,
    boxHullGap_eq_of_mem (fun _ => (1 : ℝ)) (fun _ => rho) (fun _ => hrho.le) _ p hp]
  congr 1
  funext q
  exact (congrArg f (hcomm q)).symm

/-- PB24, hull-gap half: the gap of the original polynomial on the original box
equals the gap of its expansion on `[1, rho]^n`. -/
theorem boxHullGap_originalBox_expansion {rho : ℝ} (hrho : 1 < rho)
    (S : Finset (Finset I)) (a : Finset I → ℝ) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) {x : I → ℝ}
    (hx : x ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) :
    boxHullGap l u (supportPolynomial S a) (originalBoxPoint rho l u x) =
      boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho)
        (supportPolynomial (boxExpansionSupports S)
          (originalPolynomialCoefficient rho l u S a)) x := by
  rw [boxHullGap_originalBoxPoint hrho hl hlu _ hx]
  congr 1
  funext y
  exact supportPolynomial_originalBox_expansion rho l u y S a

/-- The gap of one original monomial on the original box is at most the sum of
the gaps of its expanded monomials on `[1, rho]^n`.  This is the envelope
statement `boxHullGap_sum_le` applied to the expansion of PB23. -/
theorem boxHullGap_monomial_le_expansion {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (hasp : ∀ i, u i ≤ rho * l i)
    (s : Finset I) {x : I → ℝ}
    (hx : x ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) :
    boxHullGap l u (monomial s) (originalBoxPoint rho l u x) ≤
      ∑ t ∈ s.powerset, originalExpansionCoefficient rho l u s t *
        boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (monomial t) x := by
  have hlu' : ∀ _ : I, (1 : ℝ) ≤ rho := fun _ => hrho.le
  have hg : ∀ t ∈ s.powerset, SeparatelyAffine
      (fun q => originalExpansionCoefficient rho l u s t *
        monomial t (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q)) :=
    fun t _ => separatelyAffine_const_mul_box_monomial _ _ _ t
  have hsum := boxHullGap_sum_le s.powerset
    (fun t y => originalExpansionCoefficient rho l u s t * monomial t y)
    (fun _ => (1 : ℝ)) (fun _ => rho) hlu' hg x hx
  have hexp : (fun y => ∑ t ∈ s.powerset,
      originalExpansionCoefficient rho l u s t * monomial t y) =
      fun y => monomial s (originalBoxPoint rho l u y) := by
    funext y
    exact (monomial_originalBox_expansion rho l u y s).symm
  rw [hexp] at hsum
  rw [boxHullGap_originalBoxPoint hrho hl hlu _ hx]
  refine hsum.trans_eq (Finset.sum_congr rfl fun t _ => ?_)
  exact boxHullGap_monomial_scale t (fun _ => (1 : ℝ)) (fun _ => rho) x hlu' hx
    (originalExpansionCoefficient rho l u s t)
    (originalExpansionCoefficient_nonneg hrho hl hlu hasp s t)

/-- PB24, termwise half: the termwise gap of the original polynomial on the
original box is at most the termwise gap of its expansion on `[1, rho]^n`. -/
theorem boxTermwiseGap_originalBox_le_expansion {rho : ℝ} (hrho : 1 < rho)
    (S : Finset (Finset I)) (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (hasp : ∀ i, u i ≤ rho * l i)
    {x : I → ℝ} (hx : x ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) :
    boxTermwiseGap S a l u (originalBoxPoint rho l u x) ≤
      boxTermwiseGap (boxExpansionSupports S) (originalPolynomialCoefficient rho l u S a)
        (fun _ => (1 : ℝ)) (fun _ => rho) x := by
  simp only [boxTermwiseGap, originalPolynomialCoefficient]
  rw [boxPolynomialExpansion_sum]
  refine Finset.sum_le_sum fun s hs => mul_le_mul_of_nonneg_left ?_ (ha s hs)
  refine (boxHullGap_monomial_le_expansion hrho hl hlu hasp s hx).trans_eq ?_
  exact Finset.sum_congr rfl fun t _ => by rw [originalExpansionCoefficient_eq]

end Gaps

/-! ## The transfer step

PB23 and PB24 combined.  What is assumed here is the common-aspect bound on
`[1, rho]^n` (PB22), which this file does not prove; what is concluded is the
uniform bound on every strictly positive box of aspect ratio at most `rho`.
Fixed coordinates need not be removed, because only the surjectivity of the
transfer map is used. -/

section Assembly

/-- The transfer step of PB25: a uniform termwise-to-hull bound on the
common-aspect boxes `[1, rho]^n` is a `PositiveBoxAspectBound`. -/
theorem originalBox_bound_of_commonAspect_bound {rho U : ℝ} (hrho : 1 < rho)
    (hcommon : ∀ (K : Type) [Fintype K] [DecidableEq K]
      (T : Finset (Finset K)) (b : Finset K → ℝ) (y : K → ℝ),
      (∀ t ∈ T, 0 ≤ b t) → y ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho) →
        boxTermwiseGap T b (fun _ => (1 : ℝ)) (fun _ => rho) y ≤
          U * boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (supportPolynomial T b) y) :
    PositiveBoxAspectBound rho U := by
  intro K _ _ S a l u z ha hl hlu hasp hz
  obtain ⟨x, hx, rfl⟩ := exists_originalBoxPoint hrho hl hlu hz
  refine (boxTermwiseGap_originalBox_le_expansion hrho S a ha hl hlu hasp hx).trans ?_
  refine le_trans (hcommon K _ _ x
    (fun t _ => originalPolynomialCoefficient_nonneg hrho S a ha hl hlu hasp t) hx) ?_
  exact le_of_eq (congrArg (fun w => U * w)
    (boxHullGap_originalBox_expansion hrho S a hl hlu hx).symm)

end Assembly

end
end MultilinearGap
