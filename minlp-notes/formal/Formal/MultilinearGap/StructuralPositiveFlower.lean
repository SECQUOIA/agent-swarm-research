import Formal.MultilinearGap.StructuralSharpness
import Formal.MultilinearGap.RadixHullGap

/-! Positive-box flower witnesses, with their original polynomial graph envelopes. -/
namespace MultilinearGap.StructuralPositiveFlower
open CubicGap StructuralSharpness
noncomputable section
abbrev V (n : ℕ) := Vertex (Coord n)
def failures (n : ℕ) (v : V n) : ℕ := Radix.failCount (leafSupport n) v
def leaf (n : ℕ) (ε : ℝ) (y : Coord n → ℝ) : ℝ :=
  monomial (leafSupport n) (boxPoint (fun _ => ε) (fun _ => 1) y)
def reduced (n : ℕ) (ε : ℝ) (y : Coord n → ℝ) : ℝ :=
  (1-ε) * ∑ i : Fin n, monomial (pairSupport i) y + leaf n ε y
def correction (n : ℕ) (ε : ℝ) : ℝ := (1-ε^n)/(n:ℝ)
def payoff (n : ℕ) (ε : ℝ) (v : V n) : ℝ :=
  (1-ε) * vertexPoint v none * failures n v + 1-ε^failures n v

theorem leaf_affine (n : ℕ) (ε : ℝ) : SeparatelyAffine (leaf n ε) :=
  separatelyAffine_box_monomial _ _ _
theorem reduced_affine (n : ℕ) (ε : ℝ) : SeparatelyAffine (reduced n ε) := by
  intro x i t
  simp only [reduced]
  rw [leaf_affine n ε x i t]
  simp_rw [monomial_coordinate_affine _ x i t]
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum]
  ring

theorem leaf_vertex (n : ℕ) (ε : ℝ) (v : V n) :
    leaf n ε (vertexPoint v) = ε ^ failures n v := Radix.monomial_physVertex _ _ _
theorem leaf_card (n : ℕ) : (leafSupport n).card = n := by
  rw [leafSupport, Finset.card_image_of_injective _ (Option.some_injective _)]
  simp
theorem failures_le (n : ℕ) (v : V n) : failures n v ≤ n := by
  simpa [failures, Radix.failCount, leaf_card] using
    Finset.card_filter_le (leafSupport n) (fun i => v i = false)
theorem failures_cast (n : ℕ) (v : V n) :
    (failures n v : ℝ) = (n:ℝ) - ∑ i : Fin n, vertexPoint v (some i) := by
  have hp : (leafSupport n).filter (fun i => v i = false) =
      (leafSupport n).filter (fun i => ¬v i = true) := by
    ext i; cases v i <;> simp
  have hc := Finset.card_filter_add_card_filter_not
    (s := leafSupport n) (p := fun i => v i = true)
  have hs : (countOn (leafSupport n) v : ℝ) = ∑ i : Fin n, vertexPoint v (some i) := by
    rw [countOn_eq_sum, leafSupport, Finset.sum_image (fun _ _ _ _ h => Option.some.inj h)]
  have hcast : (countOn (leafSupport n) v : ℝ) + failures n v = n := by
    exact_mod_cast (by simpa [countOn, failures, Radix.failCount, hp, leaf_card] using hc)
  linarith
theorem expect_failures (n : ℕ) (hn : 2 ≤ n) (μ : Law (V n))
    (hm : HasMeans μ (means n)) : μ.expect (fun v => (failures n v : ℝ)) = 1 := by
  have hn0 : (n:ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
  have hm' : ∀ i, μ.expect (fun v => vertexPoint v i) = means n i := hm
  simp only [failures_cast, Law.expect_sub, Law.expect_const, Law.expect_sum, hm',
    means, Option.elim', Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  field_simp
  ring

def thresholdAtom (n : ℕ) (t : Fin 3) : V n :=
  Option.elim' (decide (t = 2)) (fun _ => decide (t ≠ 0))
def threeLaw (n : ℕ) (hn : 2 ≤ n) : Law (Fin 3) where
  weight t := if t = 1 then 1-2/(n:ℝ) else 1/(n:ℝ)
  nonneg t := by
    have h := reciprocal_bounds n hn
    split
    · rw [show 2/(n:ℝ) = 2*(1/(n:ℝ)) by ring]; linarith
    · exact h.1
  mass_one := by simp [Fin.sum_univ_succ]; ring
def threshold (n : ℕ) (hn : 2 ≤ n) : Law (V n) :=
  (threeLaw n hn).map (thresholdAtom n)
theorem threshold_expect (n : ℕ) (hn : 2 ≤ n) (f : V n → ℝ) :
    (threshold n hn).expect f = f (thresholdAtom n 0)/(n:ℝ) +
      (1-2/(n:ℝ))*f (thresholdAtom n 1) + f (thresholdAtom n 2)/(n:ℝ) := by
  rw [threshold, Law.expect_map]
  simp [Law.expect, threeLaw, Fin.sum_univ_succ]
  ring
theorem threshold_means (n : ℕ) (hn : 2 ≤ n) : HasMeans (threshold n hn) (means n) := by
  intro i
  rw [threshold_expect]
  cases i <;> simp [thresholdAtom, vertexPoint, means]
  ring
@[simp] theorem leaf_threshold_zero (n : ℕ) (ε : ℝ) :
    leaf n ε (vertexPoint (thresholdAtom n 0)) = ε^n := by
  rw [leaf, monomial_leafSupport]
  simp [boxPoint, vertexPoint, thresholdAtom]
@[simp] theorem leaf_threshold_one (n : ℕ) (ε : ℝ) :
    leaf n ε (vertexPoint (thresholdAtom n 1)) = 1 := by
  rw [leaf, monomial_leafSupport]
  simp [boxPoint, vertexPoint, thresholdAtom]
@[simp] theorem leaf_threshold_two (n : ℕ) (ε : ℝ) :
    leaf n ε (vertexPoint (thresholdAtom n 2)) = 1 := by
  rw [leaf, monomial_leafSupport]
  simp [boxPoint, vertexPoint, thresholdAtom]
theorem expect_leaf_threshold (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) :
    (threshold n hn).expect (fun v => leaf n ε (vertexPoint v)) = 1-correction n ε := by
  rw [threshold_expect]
  simp only [leaf_threshold_zero, leaf_threshold_one, leaf_threshold_two, mul_one, correction]
  ring
theorem expect_leaf_le (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε ≤ 1)
    (μ : Law (V n)) (hm : HasMeans μ (means n)) :
    μ.expect (fun v => leaf n ε (vertexPoint v)) ≤ 1-correction n ε := by
  have hnpos : (0:ℝ) < n := by exact_mod_cast (show 0<n by omega)
  have hv (v : V n) : ε^failures n v ≤ 1 - (failures n v : ℝ)*correction n ε := by
    have h := Radix.geom_chord ε h0 h1 (failures_le n v)
    dsimp [correction]
    have hd : (failures n v : ℝ)*((1-ε^n)/(n:ℝ)) ≤ 1-ε^failures n v := by
      rw [← mul_div_assoc, div_le_iff₀ hnpos]
      nlinarith
    linarith
  have h := μ.expect_mono hv
  simp only [Law.expect_sub, Law.expect_const, Law.expect_mul_const,
    expect_failures n hn μ hm, one_mul] at h
  simpa only [leaf_vertex] using h
theorem leaf_maximum (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε ≤ 1) :
    IsGreatest (envelopeValues (leaf n ε) (means n)) (1-correction n ε) := by
  apply maximum_from_laws _ (leaf_affine n ε)
  · exact fun μ hm => expect_leaf_le n hn ε h0 h1 μ hm
  · exact ⟨threshold n hn, threshold_means n hn, expect_leaf_threshold n hn ε⟩
theorem singleFail_failures (n : ℕ) (t : Fin n) : failures n (singleFailVertex n t) = 1 := by
  have h := failures_cast n (singleFailVertex n t)
  rw [singleFail_vertex_sum] at h
  have : (failures n (singleFailVertex n t):ℝ) = 1 := by linarith
  exact_mod_cast this
theorem leaf_minimum (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h0 : 0 ≤ ε) :
    IsLeast (envelopeValues (leaf n ε) (means n)) ε := by
  apply minimum_from_laws _ (leaf_affine n ε)
  · intro μ hm
    have h := μ.expect_mono (fun v => Radix.pow_ge_support_line ε h0 (failures n v))
    simp only [Law.expect_sub, Law.expect_const, Law.expect_const_mul,
      expect_failures n hn μ hm, sub_self, mul_zero, sub_zero] at h
    simpa only [leaf_vertex] using h
  · refine ⟨singleFailLaw n (by omega), singleFailLaw_means n hn, ?_⟩
    rw [singleFailLaw_expect]
    simp only [leaf_vertex, singleFail_failures, pow_one, Finset.sum_const,
      Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    have hn0 : (n:ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
    field_simp
theorem leaf_gap (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε ≤ 1) :
    hullGap (leaf n ε) (means n) = (1-ε)-correction n ε := by
  rw [hullGap, (leaf_maximum n hn ε h0 h1).csSup_eq, (leaf_minimum n hn ε h0).csInf_eq]
  ring


theorem threshold_pair (n : ℕ) (hn : 2 ≤ n) (i : Fin n) :
    (threshold n hn).expect (fun v => monomial (pairSupport i) (vertexPoint v)) = 1/n := by
  rw [threshold_expect]
  simp [monomial_pairSupport, vertexPoint, thresholdAtom]

theorem reduced_maximum (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε ≤ 1) :
    IsGreatest (envelopeValues (reduced n ε) (means n)) ((1-ε)+1-correction n ε) := by
  have hn0 : (n:ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
  have hs : (∑ i : Fin n, 1/(n:ℝ)) = 1 := by simp [hn0]
  apply maximum_from_laws _ (reduced_affine n ε)
  · intro μ hm
    have hp (i : Fin n) : μ.expect (fun v => monomial (pairSupport i) (vertexPoint v)) ≤ 1/n := by
      have hv (v : V n) : monomial (pairSupport i) (vertexPoint v) ≤ vertexPoint v none := by
        apply monomial_le_coordinate _ (fun j _ => ?_) (by simp [pairSupport])
        cases hv : v j <;> norm_num [vertexPoint, hv]
      simpa only [hm none, means, Option.elim'] using μ.expect_mono hv
    have hsum := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) => hp i)
    rw [hs] at hsum
    have hl := expect_leaf_le n hn ε h0 h1 μ hm
    simp only [reduced, Law.expect_add, Law.expect_const_mul, Law.expect_sum]
    nlinarith
  · refine ⟨threshold n hn, threshold_means n hn, ?_⟩
    simp only [reduced, Law.expect_add, Law.expect_const_mul, Law.expect_sum,
      threshold_pair, hs, expect_leaf_threshold]
    ring

theorem reduced_add_payoff (n : ℕ) (ε : ℝ) (v : V n) :
    reduced n ε (vertexPoint v) + payoff n ε v =
      (1-ε)*(n:ℝ)*vertexPoint v none + 1 := by
  simp only [reduced, monomial_pairSupport, ← Finset.mul_sum, payoff,
    leaf_vertex, failures_cast]
  ring

theorem expect_reduced_payoff (n : ℕ) (hn : 2 ≤ n) (ε : ℝ)
    (μ : Law (V n)) (hm : HasMeans μ (means n)) :
    μ.expect (fun v => reduced n ε (vertexPoint v)) =
      (1-ε)+1-μ.expect (payoff n ε) := by
  have hn0 : (n:ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
  have h := congrArg μ.expect (funext (reduced_add_payoff n ε))
  simp only [Law.expect_add, Law.expect_const_mul, Law.expect_const, hm none,
    means, Option.elim'] at h
  have hc : (1-ε)*(n:ℝ)*(1/(n:ℝ)) = 1-ε := by field_simp
  rw [hc] at h
  linarith

def payoffValues (n : ℕ) (ε : ℝ) : Set ℝ :=
  {z | ∃ μ : Law (V n), HasMeans μ (means n) ∧ μ.expect (payoff n ε) = z}

/-- The source's exact maximization formula for the actual reduced graph hull. -/
theorem hullGap_payoff_maximum (n : ℕ) (hn : 2 ≤ n) (ε : ℝ)
    (h0 : 0 ≤ ε) (h1 : ε ≤ 1) :
    IsGreatest (payoffValues n ε) (hullGap (reduced n ε) (means n)+correction n ε) := by
  have hf := reduced_affine n ε
  have hx := means_mem_cube n hn
  have he := (envelopeValues_endpoints _ hf _ hx).1
  have hv : (1-ε)+1-sInf (envelopeValues (reduced n ε) (means n)) =
      hullGap (reduced n ε) (means n)+correction n ε := by
    rw [hullGap, (reduced_maximum n hn ε h0 h1).csSup_eq]
    ring
  constructor
  · obtain ⟨μ, hm, hvμ⟩ := (mem_cubeGraph_hull_iff _ hf _ _).mp he.1
    refine ⟨μ, hm, ?_⟩
    have hh := expect_reduced_payoff n hn ε μ hm
    linarith
  · rintro z ⟨μ, hm, rfl⟩
    have hmem := (mem_cubeGraph_hull_iff _ hf _ _).mpr ⟨μ, hm, rfl⟩
    have hh := he.2 hmem
    rw [expect_reduced_payoff n hn ε μ hm] at hh
    linarith

/-- The truncation estimate as one pointwise bound; taking expectations uses
only the two prescribed first moments. -/
theorem payoff_bound (n : ℕ) (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε ≤ 1)
    (M : ℝ) (hM : 0 < M) (v : V n) :
    payoff n ε v ≤ (1-ε)*(failures n v : ℝ) +
      (1-ε)*M*vertexPoint v none + (failures n v : ℝ)/M := by
  have hA : 0 ≤ vertexPoint v none ∧ vertexPoint v none ≤ 1 := by
    cases hv : v none <;> norm_num [vertexPoint, hv]
  have hr : (0:ℝ) ≤ failures n v := Nat.cast_nonneg _
  have hg := Radix.one_sub_pow_le_mul ε h0 h1 (failures n v)
  have hpow := pow_nonneg h0 (failures n v)
  have hdiv := div_nonneg hr hM.le
  have ha : 0 ≤ 1-ε := by linarith
  unfold payoff
  by_cases hrM : (failures n v : ℝ) ≤ M
  · have hmul : (1-ε)*vertexPoint v none*(failures n v : ℝ) ≤
        (1-ε)*vertexPoint v none*M := mul_le_mul_of_nonneg_left hrM (mul_nonneg ha hA.1)
    nlinarith
  · have hdiv1 : 1 ≤ (failures n v : ℝ)/M := (le_div_iff₀ hM).mpr (by linarith)
    have hmul : (1-ε)*vertexPoint v none*(failures n v : ℝ) ≤
        (1-ε)*(failures n v : ℝ) := by nlinarith [mul_nonneg ha hr]
    nlinarith [mul_nonneg (mul_nonneg ha hM.le) hA.1]

theorem hullGap_upper (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε ≤ 1)
    (M : ℝ) (hM : 0 < M) :
    hullGap (reduced n ε) (means n) ≤ (1-ε)+(1-ε)*M/n+1/M-correction n ε := by
  obtain ⟨μ, hm, hv⟩ := (hullGap_payoff_maximum n hn ε h0 h1).1
  have h := μ.expect_mono (payoff_bound n ε h0 h1 M hM)
  simp only [Law.expect_add, Law.expect_const_mul, Law.expect_div_const,
    expect_failures n hn μ hm, hm none, means, Option.elim', mul_one] at h
  rw [hv] at h
  convert (show hullGap (reduced n ε) (means n) ≤
    (1-ε)+(1-ε)*M*(1/(n:ℝ))+1/M-correction n ε by linarith) using 1
  ring

theorem hullGap_lower (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε ≤ 1) :
    (1-ε)+(1-ε)/n-correction n ε ≤ hullGap (reduced n ε) (means n) := by
  have hmean := singleFailLaw_means n hn none
  have he : (singleFailLaw n (by omega)).expect (payoff n ε) = (1-ε)+(1-ε)/n := by
    rw [singleFailLaw_expect]
    simp only [payoff, singleFail_failures, Nat.cast_one, mul_one, pow_one]
    rw [Finset.sum_sub_distrib, Finset.sum_add_distrib, ← Finset.mul_sum]
    rw [singleFailLaw_expect] at hmean
    simp only [means, Option.elim'] at hmean
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one]
    have hn0 : (n:ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
    field_simp at hmean ⊢
    nlinarith
  have h := (hullGap_payoff_maximum n hn ε h0 h1).2
    (show (1-ε)+(1-ε)/n ∈ payoffValues n ε from
      ⟨singleFailLaw n (by omega), singleFailLaw_means n hn, he⟩)
  linarith



def physical (n : ℕ) (ε : ℝ) (x : Coord n → ℝ) : ℝ :=
  (1/(1-ε))*x none*(∑ i : Fin n, x (some i)) + ∏ i : Fin n, x (some i)
def physicalMeans (n : ℕ) (ε : ℝ) : Coord n → ℝ :=
  boxPoint (fun _ => ε) (fun _ => 1) (means n)
def coefficient (n : ℕ) (ε : ℝ) (s : Finset (Coord n)) : ℝ :=
  if s = leafSupport n then 1 else 1/(1-ε)

theorem physical_supportPolynomial (n : ℕ) (ε : ℝ) :
    supportPolynomial (supports n) (coefficient n ε) = physical n ε := by
  funext x
  simp only [supportPolynomial, sum_supports, coefficient, if_true,
    one_mul, monomial_leafSupport]
  have hp (i : Fin n) : ¬pairSupport i = leafSupport n := (leafSupport_not_pair i).symm
  simp only [hp, if_false, monomial_pairSupport, ← Finset.mul_sum, physical]
  ring

theorem physical_affine (n : ℕ) (ε : ℝ) : SeparatelyAffine (physical n ε) := by
  rw [← physical_supportPolynomial]
  exact supportPolynomial_coordinate_affine _ _

def remainder (n : ℕ) (ε : ℝ) (y : Coord n → ℝ) : ℝ :=
  ε^2*(n:ℝ)/(1-ε) + ε*(∑ i : Fin n, y (some i)) + ε*(n:ℝ)*y none

theorem physical_split (n : ℕ) (ε : ℝ) (h1 : ε ≠ 1) (y : Coord n → ℝ) :
    physical n ε (boxPoint (fun _ => ε) (fun _ => 1) y) =
      reduced n ε y + remainder n ε y := by
  have hα : 1-ε ≠ 0 := sub_ne_zero.mpr (Ne.symm h1)
  simp only [physical, reduced, leaf, monomial_leafSupport, monomial_pairSupport,
    remainder, boxPoint, Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, ← Finset.mul_sum]
  field_simp
  ring

theorem remainder_meanExact (n : ℕ) (ε : ℝ) : MeanExact (means n) (remainder n ε) := by
  intro μ hm
  have hm' : ∀ i, μ.expect (fun v => vertexPoint v i) = means n i := hm
  simp only [remainder, Law.expect_add, Law.expect_const, Law.expect_const_mul,
    Law.expect_sum, hm']

theorem physical_hullGap (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h1 : ε < 1) :
    boxHullGap (fun _ => ε) (fun _ => 1) (physical n ε) (physicalMeans n ε) =
      hullGap (reduced n ε) (means n) := by
  rw [physicalMeans, boxHullGap_eq_of_mem _ _ (fun _ => h1.le) _ _ (means_mem_cube n hn)]
  have h := hullGap_of_meanExact_split (reduced n ε) (remainder n ε)
    (fun y => physical n ε (boxPoint (fun _ => ε) (fun _ => 1) y))
    (reduced_affine n ε) (separatelyAffine_boxPoint _ (physical_affine n ε) _ _)
    (means n) (means_mem_cube n hn) 1 (by norm_num)
    (fun y => by simpa using physical_split n ε h1.ne y) (remainder_meanExact n ε)
  simpa only [one_mul] using h

theorem physical_pair_gap (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h1 : ε ≤ 1) (i : Fin n) :
    boxHullGap (fun _ => ε) (fun _ => 1) (monomial (pairSupport i)) (physicalMeans n ε) =
      (1-ε)^2/n := by
  rw [physicalMeans, boxHullGap_eq_of_mem _ _ (fun _ => h1) _ _ (means_mem_cube n hn)]
  let r : (Coord n → ℝ) → ℝ := fun y => ε^2+ε*(1-ε)*(y none+y (some i))
  have hm : MeanExact (means n) r := by
    intro μ hm
    simp only [r, Law.expect_add, Law.expect_const, Law.expect_const_mul, hm none, hm (some i)]
  have hs (y : Coord n → ℝ) : monomial (pairSupport i) (boxPoint (fun _ => ε) (fun _ => 1) y) =
      (1-ε)^2*monomial (pairSupport i) y + r y := by
    simp only [monomial_pairSupport, boxPoint, r]
    ring
  rw [hullGap_of_meanExact_split _ r _ (monomial_coordinate_affine _)
    (separatelyAffine_box_monomial _ _ _) _ (means_mem_cube n hn) _ (sq_nonneg _) hs hm,
    StructuralSharpness.pair_gap n hn i]
  ring

theorem physical_termwiseGap (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε < 1) :
    boxTermwiseGap (supports n) (coefficient n ε) (fun _ => ε) (fun _ => 1)
      (physicalMeans n ε) = 2*(1-ε)-correction n ε := by
  have hn0 : (n:ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
  have hα : 1-ε ≠ 0 := by linarith
  have hl : boxHullGap (fun _ => ε) (fun _ => 1) (monomial (leafSupport n))
      (physicalMeans n ε) = (1-ε)-correction n ε := by
    rw [physicalMeans, boxHullGap_eq_of_mem _ _ (fun _ => h1.le) _ _ (means_mem_cube n hn)]
    exact leaf_gap n hn ε h0 h1.le
  have hp (i : Fin n) : ¬pairSupport i = leafSupport n := (leafSupport_not_pair i).symm
  simp only [boxTermwiseGap, sum_supports, coefficient, if_true, hp, if_false,
    hl, physical_pair_gap n hn ε h1.le, one_mul, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul]
  field_simp
  ring


open Filter Topology

theorem correction_nonneg (n : ℕ) (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε ≤ 1) :
    0 ≤ correction n ε :=
  div_nonneg (sub_nonneg.mpr (pow_le_one₀ h0 h1)) (Nat.cast_nonneg _)

theorem correction_le (n : ℕ) (ε : ℝ) (h0 : 0 ≤ ε) :
    correction n ε ≤ 1/(n:ℝ) :=
  div_le_div_of_nonneg_right (by linarith [pow_nonneg h0 n]) (Nat.cast_nonneg _)

theorem correction_tendsto (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε ≤ 1) :
    Tendsto (fun n => correction n ε) atTop (𝓝 0) := by
  exact tendsto_const_nhds.squeeze
    (tendsto_const_nhds.div_atTop tendsto_natCast_atTop_atTop)
    (fun n => correction_nonneg n ε h0 h1) (fun n => correction_le n ε h0)

theorem reduced_hullGap_tendsto (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε < 1) :
    Tendsto (fun n => hullGap (reduced n ε) (means n)) atTop (𝓝 (1-ε)) := by
  have hi : Tendsto (fun n : ℕ => (1-ε)/(n:ℝ)) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop tendsto_natCast_atTop_atTop
  have hs : Tendsto (fun n : ℕ => 1/Real.sqrt (n:ℝ)) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop (Real.tendsto_sqrt_atTop.comp tendsto_natCast_atTop_atTop)
  have hl : Tendsto (fun n : ℕ => (1-ε)+(1-ε)/n-correction n ε)
      atTop (𝓝 (1-ε)) := by
    simpa using (tendsto_const_nhds.add hi).sub (correction_tendsto ε h0 h1.le)
  have hu : Tendsto (fun n : ℕ => (1-ε)+(1-ε)*(1/Real.sqrt (n:ℝ))+
      1/Real.sqrt (n:ℝ)-correction n ε) atTop (𝓝 (1-ε)) := by
    simpa using ((tendsto_const_nhds.add (tendsto_const_nhds.mul hs)).add hs).sub
      (correction_tendsto ε h0 h1.le)
  apply hl.squeeze' hu
  · filter_upwards [eventually_ge_atTop 2] with n hn
    exact hullGap_lower n hn ε h0 h1.le
  · filter_upwards [eventually_ge_atTop 2] with n hn
    have hnpos : (0:ℝ) < n := by exact_mod_cast (show 0<n by omega)
    have hspos := Real.sqrt_pos.mpr hnpos
    have he : (1-ε)*Real.sqrt (n:ℝ)/(n:ℝ) = (1-ε)*(1/Real.sqrt (n:ℝ)) := by
      field_simp
      nlinarith [Real.sq_sqrt hnpos.le]
    simpa only [he] using hullGap_upper n hn ε h0 h1.le _ hspos

theorem physical_hullGap_tendsto (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε < 1) :
    Tendsto (fun n => boxHullGap (fun _ => ε) (fun _ => 1) (physical n ε)
      (physicalMeans n ε)) atTop (𝓝 (1-ε)) := by
  apply (reduced_hullGap_tendsto ε h0 h1).congr'
  filter_upwards [eventually_ge_atTop 2] with n hn
  exact (physical_hullGap n hn ε h1).symm

theorem physical_termwiseGap_tendsto (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε < 1) :
    Tendsto (fun n => boxTermwiseGap (supports n) (coefficient n ε)
      (fun _ => ε) (fun _ => 1) (physicalMeans n ε)) atTop (𝓝 (2*(1-ε))) := by
  have h : Tendsto (fun n => 2*(1-ε)-correction n ε) atTop (𝓝 (2*(1-ε))) := by
    simpa using tendsto_const_nhds.sub (correction_tendsto ε h0 h1.le)
  apply h.congr'
  filter_upwards [eventually_ge_atTop 2] with n hn
  exact (physical_termwiseGap n hn ε h0 h1).symm

theorem physical_hullGap_eventually_pos (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε < 1) :
    ∀ᶠ n in atTop, 0 < boxHullGap (fun _ => ε) (fun _ => 1) (physical n ε)
      (physicalMeans n ε) :=
  (physical_hullGap_tendsto ε h0 h1).eventually (eventually_gt_nhds (by linarith))

theorem physical_ratio_tendsto (ε : ℝ) (h0 : 0 ≤ ε) (h1 : ε < 1) :
    Tendsto (fun n => boxTermwiseGap (supports n) (coefficient n ε)
      (fun _ => ε) (fun _ => 1) (physicalMeans n ε) /
      boxHullGap (fun _ => ε) (fun _ => 1) (physical n ε) (physicalMeans n ε))
      atTop (𝓝 2) := by
  have h := (physical_termwiseGap_tendsto ε h0 h1).div
    (physical_hullGap_tendsto ε h0 h1) (by linarith : 1-ε ≠ 0)
  rw [mul_div_cancel_right₀ _ (by linarith : 1-ε ≠ 0)] at h
  convert h using 1
  funext n
  rfl


/-- Coefficients after mapping the original physical box to `[1,ρ]`.
The original factor scopes are retained. -/
def scaledCoefficient (n : ℕ) (ρ : ℝ) (s : Finset (Coord n)) : ℝ :=
  coefficient n (1/ρ) s / ρ^s.card

def scaledPhysical (n : ℕ) (ρ : ℝ) : (Coord n → ℝ) → ℝ :=
  supportPolynomial (supports n) (scaledCoefficient n ρ)

def scaledMeans (n : ℕ) (ρ : ℝ) : Coord n → ℝ :=
  boxPoint (fun _ => 1) (fun _ => ρ) (means n)

theorem scaledCoefficient_pos (n : ℕ) (ρ : ℝ) (hρ : 1 < ρ) (s : Finset (Coord n)) :
    0 < scaledCoefficient n ρ s := by
  have hp : 0 < ρ := by linarith
  have he : 1/ρ < 1 := (div_lt_one hp).mpr hρ
  unfold scaledCoefficient coefficient
  split <;> positivity

theorem scaledPhysical_eq (n : ℕ) (ρ : ℝ) (x : Coord n → ℝ) :
    scaledPhysical n ρ x = physical n (1/ρ) (fun i => x i/ρ) := by
  rw [← physical_supportPolynomial]
  simp only [scaledPhysical, supportPolynomial, scaledCoefficient, monomial,
    Finset.prod_div_distrib, Finset.prod_const]
  apply Finset.sum_congr rfl
  intro s hs
  ring

theorem scaled_boxPoint (n : ℕ) (ρ : ℝ) (hρ : 1 < ρ) (y : Coord n → ℝ) :
    (fun i => boxPoint (fun _ => 1) (fun _ => ρ) y i/ρ) =
      boxPoint (fun _ => 1/ρ) (fun _ => 1) y := by
  funext i
  dsimp [boxPoint]
  have : ρ ≠ 0 := by linarith
  field_simp

theorem scaled_hullGap (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ) :
    boxHullGap (fun _ => 1) (fun _ => ρ) (scaledPhysical n ρ) (scaledMeans n ρ) =
      boxHullGap (fun _ => 1/ρ) (fun _ => 1) (physical n (1/ρ)) (physicalMeans n (1/ρ)) := by
  have hp : 0 < ρ := by linarith
  have he : 1/ρ ≤ 1 := (div_le_one hp).mpr hρ.le
  rw [scaledMeans, physicalMeans,
    boxHullGap_eq_of_mem _ _ (fun _ => hρ.le) _ _ (means_mem_cube n hn),
    boxHullGap_eq_of_mem _ _ (fun _ => he) _ _ (means_mem_cube n hn)]
  congr 1
  funext y
  rw [scaledPhysical_eq, scaled_boxPoint n ρ hρ]

theorem scaled_monomial_gap (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ)
    (s : Finset (Coord n)) :
    boxHullGap (fun _ => 1/ρ) (fun _ => 1) (monomial s) (physicalMeans n (1/ρ)) =
      (1/ρ^s.card) * boxHullGap (fun _ => 1) (fun _ => ρ) (monomial s) (scaledMeans n ρ) := by
  have hp : 0 < ρ := by linarith
  have he : 1/ρ ≤ 1 := (div_le_one hp).mpr hρ.le
  rw [physicalMeans, scaledMeans,
    boxHullGap_eq_of_mem _ _ (fun _ => he) _ _ (means_mem_cube n hn),
    boxHullGap_eq_of_mem _ _ (fun _ => hρ.le) _ _ (means_mem_cube n hn)]
  have hf : (fun y => monomial s (boxPoint (fun _ => 1/ρ) (fun _ => 1) y)) =
      (fun y => (1/ρ^s.card) * monomial s (boxPoint (fun _ => 1) (fun _ => ρ) y)) := by
    funext y
    rw [← scaled_boxPoint n ρ hρ y]
    simp only [monomial, Finset.prod_div_distrib, Finset.prod_const]
    ring
  rw [hf]
  exact hullGap_scale _ (separatelyAffine_box_monomial _ _ _) _ (means_mem_cube n hn)
    _ (by positivity)

theorem scaled_termwiseGap (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ) :
    boxTermwiseGap (supports n) (scaledCoefficient n ρ) (fun _ => 1) (fun _ => ρ)
      (scaledMeans n ρ) =
    boxTermwiseGap (supports n) (coefficient n (1/ρ)) (fun _ => 1/ρ) (fun _ => 1)
      (physicalMeans n (1/ρ)) := by
  unfold boxTermwiseGap
  apply Finset.sum_congr rfl
  intro s hs
  rw [scaled_monomial_gap n hn ρ hρ]
  dsimp [scaledCoefficient]
  ring

theorem scaled_ratio_tendsto (ρ : ℝ) (hρ : 1 < ρ) :
    Tendsto (fun n => boxTermwiseGap (supports n) (scaledCoefficient n ρ)
      (fun _ => 1) (fun _ => ρ) (scaledMeans n ρ) /
      boxHullGap (fun _ => 1) (fun _ => ρ) (scaledPhysical n ρ) (scaledMeans n ρ))
      atTop (𝓝 2) := by
  have hp : 0 < ρ := by linarith
  apply (physical_ratio_tendsto (1/ρ) (by positivity) ((div_lt_one hp).mpr hρ)).congr'
  filter_upwards [eventually_ge_atTop 2] with n hn
  rw [scaled_hullGap n hn ρ hρ, scaled_termwiseGap n hn ρ hρ]

theorem scaled_hullGap_eventually_pos (ρ : ℝ) (hρ : 1 < ρ) :
    ∀ᶠ n in atTop, 0 < boxHullGap (fun _ => 1) (fun _ => ρ)
      (scaledPhysical n ρ) (scaledMeans n ρ) := by
  have hp : 0 < ρ := by linarith
  filter_upwards [eventually_ge_atTop 2,
    physical_hullGap_eventually_pos (1/ρ) (by positivity) ((div_lt_one hp).mpr hρ)] with n hn hh
  rwa [scaled_hullGap n hn ρ hρ]

/-- Every uniform upper constant on this fixed positive box is at least two. -/
theorem scaled_universal_constant_ge_two (ρ : ℝ) (hρ : 1 < ρ) (C : ℝ)
    (hC : ∀ n : ℕ, 2 ≤ n →
      boxTermwiseGap (supports n) (scaledCoefficient n ρ) (fun _ => 1) (fun _ => ρ)
        (scaledMeans n ρ) ≤
      C * boxHullGap (fun _ => 1) (fun _ => ρ) (scaledPhysical n ρ) (scaledMeans n ρ)) :
    2 ≤ C := by
  apply le_of_tendsto (scaled_ratio_tendsto ρ hρ)
  filter_upwards [eventually_ge_atTop 2, scaled_hullGap_eventually_pos ρ hρ] with n hn hp
  exact (div_le_iff₀ hp).mpr (hC n hn)


theorem physical_payoff_maximum (n : ℕ) (hn : 2 ≤ n) (ε : ℝ)
    (h0 : 0 ≤ ε) (h1 : ε < 1) :
    IsGreatest (payoffValues n ε)
      (boxHullGap (fun _ => ε) (fun _ => 1) (physical n ε) (physicalMeans n ε)
        + correction n ε) := by
  rw [physical_hullGap n hn ε h1]
  exact hullGap_payoff_maximum n hn ε h0 h1.le

theorem means_strict (n : ℕ) (hn : 2 ≤ n) (i : Coord n) :
    0 < means n i ∧ means n i < 1 := by
  have hp : (0:ℝ) < n := by exact_mod_cast (show 0<n by omega)
  have hrec : (0:ℝ) < 1/n := by positivity
  have hbound := (reciprocal_bounds n hn).2
  cases i <;> simp only [means, Option.elim'] <;> constructor <;> linarith

theorem physicalMeans_strict (n : ℕ) (hn : 2 ≤ n) (ε : ℝ) (h1 : ε < 1)
    (i : Coord n) : ε < physicalMeans n ε i ∧ physicalMeans n ε i < 1 := by
  have hi := means_strict n hn i
  dsimp [physicalMeans, boxPoint]
  constructor <;> nlinarith

theorem scaledMeans_strict (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ)
    (i : Coord n) : 1 < scaledMeans n ρ i ∧ scaledMeans n ρ i < ρ := by
  have hi := means_strict n hn i
  dsimp [scaledMeans, boxPoint]
  constructor <;> nlinarith

end
end MultilinearGap.StructuralPositiveFlower
