import Formal.MultilinearGap.Attainment

/-! Bridges between the paper's original-term definition and box graph-hull widths. -/
namespace MultilinearGap
noncomputable section
open CubicGap
variable {I J : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] in
/-- Finite sums preserve separate affinity. -/
theorem separatelyAffine_sum (S : Finset J) (f : J → (I → ℝ) → ℝ)
    (hf : ∀ j ∈ S, SeparatelyAffine (f j)) :
    SeparatelyAffine (fun y => ∑ j ∈ S, f j y) := by
  intro y i t
  simp only
  simp_rw [Finset.mul_sum, ← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl fun j hj => hf j hj y i t

omit [Fintype I] in
/-- Scaling preserves the entire attainable slice, before taking endpoints. -/
theorem envelopeValues_scale [Finite I] (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (c : ℝ) :
    envelopeValues (fun y => c * f y) x = (fun z => c * z) '' envelopeValues f x := by
  let := Fintype.ofFinite I
  have hcf : SeparatelyAffine (fun y => c * f y) := by
    intro y i t
    dsimp only
    rw [hf]
    ring
  ext z
  constructor
  · intro hz
    obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff _ hcf x z).mp hz
    rw [Law.expect_const_mul] at hv
    exact ⟨μ.expect (fun v => f (vertexPoint v)),
      (mem_cubeGraph_hull_iff _ hf x _).mpr ⟨μ, hm, rfl⟩, hv⟩
  · rintro ⟨q, hq, rfl⟩
    obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff _ hf x q).mp hq
    exact (mem_cubeGraph_hull_iff _ hcf x _).mpr
      ⟨μ, hm, by rw [Law.expect_const_mul, hv]⟩

/-- Nonnegative scaling scales the actual graph-hull width. -/
theorem hullGap_scale (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (hx : x ∈ cube I) (c : ℝ) (hc : 0 ≤ c) :
    hullGap (fun y => c * f y) x = c * hullGap f x := by
  have hne := envelopeValues_nonempty f x hx
  have hcompact := envelopeValues_isCompact f hf x
  rw [hullGap, envelopeValues_scale f hf]
  rcases eq_or_lt_of_le hc with hzero | hpos
  · subst c
    simp [hne.image_const]
  · have hsup := (OrderIso.mulLeft₀ c hpos).map_csSup' hne hcompact.bddAbove
    have hinf := (OrderIso.mulLeft₀ c hpos).map_csInf' hne hcompact.bddBelow
    change c * sSup (envelopeValues f x) =
      sSup ((fun z => c * z) '' envelopeValues f x) at hsup
    change c * sInf (envelopeValues f x) =
      sInf ((fun z => c * z) '' envelopeValues f x) at hinf
    rw [← hsup, ← hinf, hullGap, mul_sub]

/-- Convexifying a sum together cannot give more width than convexifying its terms separately. -/
theorem hullGap_sum_le (S : Finset J) (f : J → (I → ℝ) → ℝ)
    (hf : ∀ j ∈ S, SeparatelyAffine (f j)) (x : I → ℝ) (hx : x ∈ cube I) :
    hullGap (fun y => ∑ j ∈ S, f j y) x ≤ ∑ j ∈ S, hullGap (f j) x := by
  have hne := envelopeValues_nonempty (fun y => ∑ j ∈ S, f j y) x hx
  have hb : ∀ z ∈ envelopeValues (fun y => ∑ j ∈ S, f j y) x,
      (∑ j ∈ S, sInf (envelopeValues (f j) x)) ≤ z ∧
      z ≤ ∑ j ∈ S, sSup (envelopeValues (f j) x) := by
    intro z hz
    obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff _ (separatelyAffine_sum S f hf) x z).mp hz
    have hexpect : μ.expect (fun v => ∑ j ∈ S, f j (vertexPoint v)) =
        ∑ j ∈ S, μ.expect (fun v => f j (vertexPoint v)) := by
      simp only [Law.expect, Finset.mul_sum]
      exact Finset.sum_comm
    have hmem (j : J) (hj : j ∈ S) :
        μ.expect (fun v => f j (vertexPoint v)) ∈ envelopeValues (f j) x :=
      (mem_cubeGraph_hull_iff _ (hf j hj) x _).mpr ⟨μ, hm, rfl⟩
    rw [← hv, hexpect]
    constructor
    · exact Finset.sum_le_sum fun j hj =>
        csInf_le (envelopeValues_isCompact (f j) (hf j hj) x).bddBelow (hmem j hj)
    · exact Finset.sum_le_sum fun j hj =>
        le_csSup (envelopeValues_isCompact (f j) (hf j hj) x).bddAbove (hmem j hj)
  have hinf := le_csInf hne (fun z hz => (hb z hz).1)
  have hsup := csSup_le hne (fun z hz => (hb z hz).2)
  simp only [hullGap, Finset.sum_sub_distrib]
  linarith

omit [Fintype I] in
theorem separatelyAffine_box_monomial (l u : I → ℝ) (s : Finset I) :
    SeparatelyAffine (fun p => monomial s (boxPoint l u p)) := by
  have he : (fun p => monomial s (boxPoint l u p)) =
      supportPolynomial s.powerset (boxExpansionCoefficient l u s) := by
    funext p
    exact monomial_box_expansion l u p s
  rw [he]
  exact supportPolynomial_coordinate_affine _ _

omit [Fintype I] [DecidableEq I] in
/-- Coefficients scale original-box term widths, including degenerate boxes. -/
theorem boxHullGap_monomial_scale [Finite I] (s : Finset I) (l u x : I → ℝ)
    (hlu : ∀ i, l i ≤ u i) (hx : x ∈ coordinateBox l u) (c : ℝ) (hc : 0 ≤ c) :
    boxHullGap l u (fun y => c * monomial s y) x =
      c * boxHullGap l u (monomial s) x := by
  classical
  let := Fintype.ofFinite I
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  rw [boxHullGap_eq_of_mem l u hlu _ p hp, boxHullGap_eq_of_mem l u hlu _ p hp]
  exact hullGap_scale _ (separatelyAffine_box_monomial l u s) p hp c hc

omit [Fintype I] [DecidableEq I] in
/-- The formal weighted definition equals the paper's sum of scaled original-term widths. -/
theorem boxTermwiseGap_eq_term_gaps [Finite I] (S : Finset (Finset I)) (a : Finset I → ℝ)
    (ha : ∀ s ∈ S, 0 ≤ a s) (l u x : I → ℝ)
    (hlu : ∀ i, l i ≤ u i) (hx : x ∈ coordinateBox l u) :
    boxTermwiseGap S a l u x =
      ∑ s ∈ S, boxHullGap l u (fun y => a s * monomial s y) x := by
  classical
  let := Fintype.ofFinite I
  exact Finset.sum_congr rfl fun s hs =>
    (boxHullGap_monomial_scale s l u x hlu hx (a s) (ha s hs)).symm

omit [Fintype I] [DecidableEq I] in
/-- The full original-box gap is nonnegative and at most its original-term relaxation gap. -/
theorem box_gap_comparison [Finite I] (S : Finset (Finset I)) (a : Finset I → ℝ)
    (ha : ∀ s ∈ S, 0 ≤ a s) (l u x : I → ℝ)
    (hlu : ∀ i, l i ≤ u i) (hx : x ∈ coordinateBox l u) :
    0 ≤ boxHullGap l u (supportPolynomial S a) x ∧
      boxHullGap l u (supportPolynomial S a) x ≤ boxTermwiseGap S a l u x := by
  classical
  let := Fintype.ofFinite I
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  let f : Finset I → (I → ℝ) → ℝ := fun s q => a s * monomial s (boxPoint l u q)
  have hf (s : Finset I) : SeparatelyAffine (f s) := by
    intro y i t
    dsimp [f]
    have he := separatelyAffine_box_monomial l u s y i t
    dsimp only at he
    rw [he]
    ring
  rw [boxHullGap_eq_of_mem l u hlu _ p hp]
  constructor
  · exact hullGap_nonneg _ (separatelyAffine_sum S f (fun s _ => hf s)) p hp
  · have h := hullGap_sum_le S f (fun s _ => hf s) p hp
    change hullGap (fun q => supportPolynomial S a (boxPoint l u q)) p ≤ _ at h
    refine h.trans_eq ?_
    unfold boxTermwiseGap
    apply Finset.sum_congr rfl
    intro s hs
    rw [boxHullGap_eq_of_mem l u hlu _ p hp]
    exact hullGap_scale _ (separatelyAffine_box_monomial l u s) p hp (a s) (ha s hs)

end
end MultilinearGap
