import Formal.CubicGap.Counts
import Formal.CubicGap.Finite
import Formal.CubicGap.Expectation
import Formal.CubicGap.HomogeneousSupports
import Formal.CubicGap.HomogeneousTermwise
import Formal.CubicGap.Envelope

namespace CubicGap
noncomputable section

abbrev HomogeneousCoordinate := (Fin 2 × Fin 16) ⊕ Fin 20

def homogeneous52 (x : HomogeneousCoordinate → ℝ) : ℝ :=
  (∑ i, x (.inl (0,i))) * elementary 2 (fun i => x (.inl (1,i))) +
    (∑ k, x (.inr k)) * elementary 2 (fun i => x (.inl (0,i)))

def homogeneousMeans : HomogeneousCoordinate → ℝ :=
  Sum.elim (fun p => if p.1 = 0 then 1/2 else 3/4) (fun _ => 999/1000)

def homogeneousValue (a c z : ℕ) : ℝ :=
  a * (c.choose 2 : ℝ) + z * (a.choose 2 : ℝ)

theorem homogeneous52_binary (v : HomogeneousCoordinate → Bool) :
    homogeneous52 (vertexPoint v) = homogeneousValue
      (count fun i => v (.inl (0,i))) (count fun i => v (.inl (1,i)))
      (count fun k => v (.inr k)) := by
  simp only [homogeneous52, vertexPoint, elementary_binary, sum_binary, homogeneousValue]

theorem homogeneous_count_minorant (a c z : ℕ) (ha : a ≤ 16) (hc : c ≤ 16)
    (hz : z ≤ 20) :
    214 * (a : ℝ) + (177 / 2 : ℝ) * c - 1686 - 120 * (20 - z) ≤
      homogeneousValue a c z := by
  have h := two_minorant16 ⟨a, by omega⟩ ⟨c, by omega⟩
  have hr : 214 * (a : ℝ) + (177 / 2 : ℝ) * c - 1686 ≤
      a * (c.choose 2 : ℝ) + 20 * (a.choose 2 : ℝ) := by
    have hh := (Rat.cast_le (K := ℝ)).mpr h
    norm_num [twoValue] at hh
    linarith
  have hchoose : (a.choose 2 : ℝ) ≤ 120 := by
    have hn := Nat.choose_le_choose 2 ha
    exact_mod_cast hn
  have hz' : (z : ℝ) ≤ 20 := by exact_mod_cast hz
  have hprod := mul_nonneg (sub_nonneg.mpr hz') (sub_nonneg.mpr hchoose)
  dsimp [homogeneousValue]
  nlinarith

theorem homogeneous_binary_minorant (v : HomogeneousCoordinate → Bool) :
    214 * (∑ i, vertexPoint v (.inl (0,i))) +
      (177 / 2 : ℝ) * (∑ i, vertexPoint v (.inl (1,i))) - 1686 -
      120 * (20 - ∑ k, vertexPoint v (.inr k)) ≤ homogeneous52 (vertexPoint v) := by
  rw [homogeneous52_binary]
  simp only [vertexPoint, sum_binary]
  apply homogeneous_count_minorant
  · simpa using count_le (fun i : Fin 16 => v (.inl (0,i)))
  · simpa using count_le (fun i : Fin 16 => v (.inl (1,i)))
  · simpa using count_le (fun k : Fin 20 => v (.inr k))


theorem homogeneous_law_lower (μ : Law (Vertex HomogeneousCoordinate))
    (hmean : ∀ i, μ.expect (fun v => vertexPoint v i) = homogeneousMeans i) :
    (1088 - 12 / 5 : ℝ) ≤ μ.expect (fun v => homogeneous52 (vertexPoint v)) := by
  have h := μ.expect_mono homogeneous_binary_minorant
  simp only [Law.expect_sub, Law.expect_add, Law.expect_const_mul, Law.expect_const,
    Law.expect_sum, hmean] at h
  norm_num [homogeneousMeans] at h ⊢
  exact h



theorem homogeneous_count_upper (a c z : ℕ) (ha : a ≤ 16) (hc : c ≤ 16)
    (hz : z ≤ 20) : homogeneousValue a c z ≤ 270 * (a : ℝ) := by
  have hc' : (c.choose 2 : ℝ) ≤ 120 := by
    exact_mod_cast Nat.choose_le_choose 2 hc
  have hz' : (z : ℝ) ≤ 20 := by exact_mod_cast hz
  have ha0 : (0 : ℝ) ≤ a := Nat.cast_nonneg a
  have hp0 : (0 : ℝ) ≤ a.choose 2 := Nat.cast_nonneg _
  have hp : (a.choose 2 : ℝ) ≤ 15 * a / 2 := by
    have hf : ∀ a : Fin 17, (a.val.choose 2 : ℚ) ≤ 15 * a.val / 2 := by
      decide +kernel
    have hh := (Rat.cast_le (K := ℝ)).mpr (hf ⟨a, by omega⟩)
    norm_num at hh
    linarith
  have ht1 := mul_le_mul_of_nonneg_left hc' ha0
  have ht2 := mul_le_mul_of_nonneg_right hz' hp0
  dsimp [homogeneousValue]
  nlinarith

theorem homogeneous_binary_upper (v : HomogeneousCoordinate → Bool) :
    homogeneous52 (vertexPoint v) ≤ 270 * (∑ i, vertexPoint v (.inl (0,i))) := by
  rw [homogeneous52_binary]
  simp only [vertexPoint, sum_binary]
  apply homogeneous_count_upper
  · simpa using count_le (fun i : Fin 16 => v (.inl (0,i)))
  · simpa using count_le (fun i : Fin 16 => v (.inl (1,i)))
  · simpa using count_le (fun k : Fin 20 => v (.inr k))

theorem homogeneous_law_upper (μ : Law (Vertex HomogeneousCoordinate))
    (hmean : ∀ i, μ.expect (fun v => vertexPoint v i) = homogeneousMeans i) :
    μ.expect (fun v => homogeneous52 (vertexPoint v)) ≤ 2160 := by
  have h := μ.expect_mono homogeneous_binary_upper
  norm_num [hmean, homogeneousMeans] at h
  exact h


theorem homogeneous52_separatelyAffine : SeparatelyAffine homogeneous52 := by
  intro x i t
  have heq : homogeneous52 = supportPolynomial homSupports (fun _ => 1) := by
    funext x
    exact (homSupports_polynomial x).symm
  rw [heq]
  exact supportPolynomial_coordinate_affine _ _ x i t

theorem homogeneous_hull_bounds (z : ℝ)
    (hz : (homogeneousMeans, z) ∈ convexHull ℝ (cubeGraph homogeneous52)) :
    1088 - 12 / 5 ≤ z ∧ z ≤ 2160 := by
  obtain ⟨μ, hmean, rfl⟩ :=
    (mem_cubeGraph_hull_iff homogeneous52 homogeneous52_separatelyAffine _ _).mp hz
  exact ⟨homogeneous_law_lower μ hmean, homogeneous_law_upper μ hmean⟩

theorem homogeneous_means_in_cube : homogeneousMeans ∈ cube HomogeneousCoordinate := by
  intro i
  rcases i with ⟨g, i⟩ | k
  · fin_cases g <;> norm_num [homogeneousMeans]
  · norm_num [homogeneousMeans]

theorem homogeneous_at_means : homogeneous52 homogeneousMeans = 5697 / 5 := by
  norm_num [homogeneous52, homogeneousMeans, elementary_const, Nat.choose]

theorem homogeneous_low_hull_point :
    (homogeneousMeans, (5697 / 5 : ℝ)) ∈ convexHull ℝ (cubeGraph homogeneous52) := by
  apply subset_convexHull
  exact ⟨homogeneous_means_in_cube, homogeneous_at_means.symm⟩


def homogeneousThreshold : Law (Fin 4) where
  weight s := if s.val = 0 then 1/1000 else if s.val = 1 then 249/1000
    else if s.val = 2 then 1/4 else 1/2
  nonneg i := by fin_cases i <;> norm_num
  mass_one := by norm_num [Fin.sum_univ_succ]

def homogeneousThresholdVertex (s : Fin 4) : Vertex HomogeneousCoordinate :=
  Sum.elim (fun p => if p.1 = 0 then decide (s.val = 3) else decide (2 ≤ s.val))
    (fun _ => decide (1 ≤ s.val))

theorem homogeneous_threshold_means (i : HomogeneousCoordinate) :
    homogeneousThreshold.expect (fun s => vertexPoint (homogeneousThresholdVertex s) i) =
      homogeneousMeans i := by
  rcases i with ⟨g, i⟩ | k
  · fin_cases g <;>
      norm_num [Law.expect, homogeneousThreshold, homogeneousThresholdVertex, vertexPoint,
        homogeneousMeans, Fin.sum_univ_succ]
  · norm_num [Law.expect, homogeneousThreshold, homogeneousThresholdVertex, vertexPoint,
      homogeneousMeans, Fin.sum_univ_succ]

theorem homogeneous_threshold_value :
    homogeneousThreshold.expect
      (fun s => homogeneous52 (vertexPoint (homogeneousThresholdVertex s))) =
      2160 := by
  norm_num [Law.expect, homogeneousThreshold, homogeneousThresholdVertex, vertexPoint,
    homogeneous52, elementary_const, Nat.choose, Fin.sum_univ_succ]

theorem homogeneous_upper_hull_point :
    (homogeneousMeans, (2160 : ℝ)) ∈ convexHull ℝ (cubeGraph homogeneous52) := by
  apply (mem_cubeGraph_hull_iff homogeneous52 homogeneous52_separatelyAffine _ _).mpr
  refine ⟨homogeneousThreshold.map homogeneousThresholdVertex, ?_, ?_⟩
  · intro i
    simpa [Function.comp_def] using homogeneous_threshold_means i
  · simpa [Function.comp_def] using homogeneous_threshold_value


/-- The actual convex envelope at all 52 prescribed means. -/
def homogeneousConvexEnvelope : ℝ := sInf (envelopeValues homogeneous52 homogeneousMeans)

theorem homogeneous_envelope_nonempty :
    (envelopeValues homogeneous52 homogeneousMeans).Nonempty :=
  ⟨2160, homogeneous_upper_hull_point⟩

theorem homogeneous_envelope_bddBelow :
    BddBelow (envelopeValues homogeneous52 homogeneousMeans) :=
  ⟨1088 - 12 / 5, fun z hz => (homogeneous_hull_bounds z hz).1⟩

theorem homogeneous_convex_envelope_bounds :
    1088 - 12 / 5 ≤ homogeneousConvexEnvelope ∧ homogeneousConvexEnvelope ≤ 5697 / 5 := by
  constructor
  · exact le_csInf homogeneous_envelope_nonempty fun z hz => (homogeneous_hull_bounds z hz).1
  · exact csInf_le homogeneous_envelope_bddBelow homogeneous_low_hull_point

theorem homogeneous_concave_envelope :
    IsGreatest (envelopeValues homogeneous52 homogeneousMeans) 2160 :=
  ⟨homogeneous_upper_hull_point, fun z hz => (homogeneous_hull_bounds z hz).2⟩

/-- The hull gap uses the actual convex envelope, not merely its lower certificate. -/
def homogeneousHullGap : ℝ := 2160 - homogeneousConvexEnvelope

theorem homogeneous_hull_gap_bounds : 0 < homogeneousHullGap ∧ homogeneousHullGap ≤ 5372 / 5 := by
  have h := homogeneous_convex_envelope_bounds
  dsimp [homogeneousHullGap]
  constructor <;> linarith

theorem homogeneous_ratio_bound : (2700 / 1343 : ℝ) ≤ 2160 / homogeneousHullGap ∧
    (2 : ℝ) < 2700 / 1343 := by
  have h := homogeneous_hull_gap_bounds
  constructor
  · apply (le_div_iff₀ h.1).mpr
    nlinarith [h.2]
  · norm_num


/-- Width of the termwise relaxation given by the standard product inequalities. -/
def homogeneousTermwiseGap : ℝ :=
  (∑ s ∈ homSupports.attach,
    s.val.inf' (homSupports_nonempty s.property) homogeneousMeans) -
  (∑ s ∈ homSupports,
    max (0 : ℝ) ((∑ j ∈ s, homogeneousMeans j) - (s.card - 1)))

theorem homogeneous_termwise_gap : homogeneousTermwiseGap = 2160 := by
  have hA : ∀ i, homogeneousMeans (homA i) = (1 / 2 : ℝ) := by
    intro i
    change homogeneousMeans (.inl (0, i)) = _
    norm_num [homogeneousMeans]
  have hC : ∀ i, homogeneousMeans (homC i) = (3 / 4 : ℝ) := by
    intro i
    change homogeneousMeans (.inl (1, i)) = _
    norm_num [homogeneousMeans]
  have hD : ∀ i, homogeneousMeans (homD i) = (999 / 1000 : ℝ) := by
    intro i; norm_num [homogeneousMeans, homD]
  rw [homogeneousTermwiseGap, homSupports_upper_total _ hA hC hD,
    homSupports_lower_total _ hA hC hD]
  norm_num

/-- A homogeneous cubic with 52 variables and 4320 distinct unit-coefficient terms
has a rigorously certified termwise-to-hull ratio strictly greater than two. -/
theorem homogeneous52_counterexample :
    Fintype.card HomogeneousCoordinate = 52 ∧ homSupports.card = 4320 ∧
    (∀ s ∈ homSupports, s.card = 3) ∧
    (∀ x, homogeneous52 x = supportPolynomial homSupports (fun _ => 1) x) ∧
    IsGreatest (envelopeValues homogeneous52 homogeneousMeans) 2160 ∧
    homogeneousTermwiseGap = 2160 ∧
    0 < homogeneousHullGap ∧ homogeneousHullGap ≤ 5372 / 5 ∧
    (2700 / 1343 : ℝ) ≤ homogeneousTermwiseGap / homogeneousHullGap ∧
    (2 : ℝ) < 2700 / 1343 := by
  refine ⟨homCoord_card, homSupports_card, fun _ hs => homSupports_degree hs,
    fun x => (homSupports_polynomial x).symm, homogeneous_concave_envelope,
    homogeneous_termwise_gap, homogeneous_hull_gap_bounds.1,
    homogeneous_hull_gap_bounds.2, ?_, homogeneous_ratio_bound.2⟩
  rw [homogeneous_termwise_gap]
  exact homogeneous_ratio_bound.1


private theorem homogeneousMeans_homA (i : Fin 16) :
    homogeneousMeans (homA i) = (1 / 2 : ℝ) := by
  change homogeneousMeans (.inl (0, i)) = _
  norm_num [homogeneousMeans]

private theorem homogeneousMeans_homC (i : Fin 16) :
    homogeneousMeans (homC i) = (3 / 4 : ℝ) := by
  change homogeneousMeans (.inl (1, i)) = _
  norm_num [homogeneousMeans]

private theorem homogeneousMeans_homD (i : Fin 20) :
    homogeneousMeans (homD i) = (999 / 1000 : ℝ) := by
  norm_num [homogeneousMeans, homD]

private theorem homogeneous_support_has_U (s : Finset HomogeneousCoordinate)
    (hs : s ∈ homSupports) : ∃ i : Fin 16, Sum.inl (0,i) ∈ s := by
  obtain ⟨_, ⟨j, hj, heq⟩, _⟩ := homSupports_means homogeneousMeans
    homogeneousMeans_homA homogeneousMeans_homC homogeneousMeans_homD hs
  rcases j with ⟨g, i⟩ | k
  · fin_cases g
    · exact ⟨i, hj⟩
    · norm_num [homogeneousMeans] at heq
  · norm_num [homogeneousMeans] at heq

theorem homogeneous_monomial_maximum (s : Finset HomogeneousCoordinate)
    (hs : s ∈ homSupports) :
    IsGreatest (envelopeValues (monomial s) homogeneousMeans) (1 / 2) := by
  obtain ⟨i, hi⟩ := homogeneous_support_has_U s hs
  apply maximum_from_laws (monomial s) (monomial_coordinate_affine s) homogeneousMeans
  · intro μ hmean
    have h := μ.expect_mono (fun v => monomial_le_coordinate s (x := vertexPoint v)
      (by intro j _; simp only [vertexPoint]; split <;> norm_num) hi)
    simpa [hmean (.inl (0,i)), homogeneousMeans] using h
  · refine ⟨homogeneousThreshold.map homogeneousThresholdVertex, ?_, ?_⟩
    · intro j
      simpa [Function.comp_def] using homogeneous_threshold_means j
    · rw [Law.expect_map]
      change homogeneousThreshold.expect
        (fun t => monomial s (vertexPoint (homogeneousThresholdVertex t))) = _
      have hv (t : Fin 4) : monomial s (vertexPoint (homogeneousThresholdVertex t)) =
          if t.val = 3 then 1 else 0 := by
        by_cases ht : t.val = 3
        · rw [if_pos ht]
          apply Finset.prod_eq_one
          intro j _
          rcases j with ⟨g, j⟩ | k
          · fin_cases g <;> norm_num [vertexPoint, homogeneousThresholdVertex, ht]
          · norm_num [vertexPoint, homogeneousThresholdVertex, ht]
        · rw [if_neg ht]
          apply Finset.prod_eq_zero hi
          simp [vertexPoint, homogeneousThresholdVertex, ht]
      simp_rw [hv]
      norm_num [homogeneousThreshold, Law.expect, Fin.sum_univ_succ]


theorem homogeneous_monomial_minimum (s : Finset HomogeneousCoordinate)
    (hs : s ∈ homSupports) :
    IsLeast (envelopeValues (monomial s) homogeneousMeans) 0 :=
  homSupports_exact_lower homogeneousMeans homogeneous_means_in_cube
    homogeneousMeans_homA homogeneousMeans_homC hs

/-- The sum of exact monomial envelope widths at the specified ambient means. -/
def homogeneousExactTermwiseGap : ℝ :=
  ∑ s ∈ homSupports, (sSup (envelopeValues (monomial s) homogeneousMeans) -
    sInf (envelopeValues (monomial s) homogeneousMeans))

theorem homogeneous_exact_termwise_gap : homogeneousExactTermwiseGap = 2160 := by
  have heq : homogeneousExactTermwiseGap = ∑ _s ∈ homSupports, (1 / 2 : ℝ) := by
    apply Finset.sum_congr rfl
    intro s hs
    rw [(homogeneous_monomial_maximum s hs).csSup_eq,
      (homogeneous_monomial_minimum s hs).csInf_eq]
    norm_num
  rw [heq]
  norm_num [homSupports_card]

theorem homogeneous_means_interior :
    ∀ i, 0 < homogeneousMeans i ∧ homogeneousMeans i < 1 := by
  intro i
  rcases i with ⟨g, i⟩ | k
  · fin_cases g <;> norm_num [homogeneousMeans]
  · norm_num [homogeneousMeans]

/-- The numerator is the sum of actual monomial envelope widths; the denominator
is the width of the actual 52-variable polynomial graph hull. -/
theorem homogeneous52_exact_envelope_ratio :
    homogeneousExactTermwiseGap = 2160 ∧
    IsGreatest (envelopeValues homogeneous52 homogeneousMeans) 2160 ∧
    0 < homogeneousHullGap ∧ homogeneousHullGap ≤ 5372 / 5 ∧
    (2700 / 1343 : ℝ) ≤ homogeneousExactTermwiseGap / homogeneousHullGap ∧
    (2 : ℝ) < homogeneousExactTermwiseGap / homogeneousHullGap := by
  refine ⟨homogeneous_exact_termwise_gap, homogeneous_concave_envelope,
    homogeneous_hull_gap_bounds.1, homogeneous_hull_gap_bounds.2, ?_, ?_⟩
  · rw [homogeneous_exact_termwise_gap]
    exact homogeneous_ratio_bound.1
  · rw [homogeneous_exact_termwise_gap]
    exact lt_of_lt_of_le homogeneous_ratio_bound.2 homogeneous_ratio_bound.1

end
end CubicGap
