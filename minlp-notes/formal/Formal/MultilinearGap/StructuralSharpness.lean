import Formal.MultilinearGap.MonomialEnvelope
import Formal.MultilinearGap.GeneralGaps

/-! The unit-coefficient feedback-one sharpness family, with actual graph-hull gaps. -/
namespace MultilinearGap.StructuralSharpness
open CubicGap
noncomputable section

abbrev Coord (n : ℕ) := Option (Fin n)
def leafSupport (n : ℕ) : Finset (Coord n) := Finset.univ.image some
def pairSupport {n : ℕ} (i : Fin n) : Finset (Coord n) := {none, some i}
def supports (n : ℕ) : Finset (Finset (Coord n)) :=
  insert (leafSupport n) (Finset.univ.image pairSupport)
def means (n : ℕ) : Coord n → ℝ := Option.elim' (1 / n) (fun _ => 1 - 1 / n)
def polynomial (n : ℕ) (x : Coord n → ℝ) : ℝ :=
  x none * (∑ i : Fin n, x (some i)) + ∏ i : Fin n, x (some i)

@[simp] theorem mem_leafSupport {n : ℕ} (i : Fin n) : some i ∈ leafSupport n := by
  simp [leafSupport]
@[simp] theorem none_not_mem_leafSupport (n : ℕ) : none ∉ leafSupport n := by
  simp [leafSupport]
theorem pairSupport_injective {n : ℕ} : Function.Injective (@pairSupport n) := by
  intro i j h
  have : some i ∈ pairSupport j := h ▸ (by simp [pairSupport])
  simpa [pairSupport] using this

theorem leafSupport_not_pair {n : ℕ} (i : Fin n) : leafSupport n ≠ pairSupport i := by
  intro h
  have : none ∈ leafSupport n := h ▸ (by simp [pairSupport])
  exact none_not_mem_leafSupport n this

theorem sum_supports (n : ℕ) (f : Finset (Coord n) → ℝ) :
    ∑ s ∈ supports n, f s = f (leafSupport n) + ∑ i : Fin n, f (pairSupport i) := by
  rw [supports, Finset.sum_insert]
  · rw [Finset.sum_image (fun i _ j _ h => pairSupport_injective h)]
  · simp only [Finset.mem_image, Finset.mem_univ, true_and, not_exists]
    intro i h
    exact leafSupport_not_pair i h.symm

@[simp] theorem monomial_leafSupport (n : ℕ) (x : Coord n → ℝ) :
    monomial (leafSupport n) x = ∏ i : Fin n, x (some i) := by
  rw [monomial, leafSupport, Finset.prod_image]
  exact fun i _ j _ h => Option.some.inj h
@[simp] theorem monomial_pairSupport {n : ℕ} (i : Fin n) (x : Coord n → ℝ) :
    monomial (pairSupport i) x = x none * x (some i) := by
  simp [monomial, pairSupport]

theorem supportPolynomial_eq (n : ℕ) :
    supportPolynomial (supports n) (fun _ => 1) = polynomial n := by
  funext x
  simp only [supportPolynomial, one_mul, sum_supports, monomial_leafSupport,
    monomial_pairSupport, polynomial, ← Finset.mul_sum]
  ring

theorem polynomial_separatelyAffine (n : ℕ) : SeparatelyAffine (polynomial n) := by
  rw [← supportPolynomial_eq]
  exact supportPolynomial_coordinate_affine _ _

theorem reciprocal_bounds (n : ℕ) (hn : 2 ≤ n) :
    0 ≤ 1 / (n : ℝ) ∧ 1 / (n : ℝ) ≤ 1 / 2 := by
  have h : (2 : ℝ) ≤ n := by exact_mod_cast hn
  exact ⟨by positivity, one_div_le_one_div_of_le (by norm_num) h⟩

theorem means_mem_cube (n : ℕ) (hn : 2 ≤ n) : means n ∈ cube (Coord n) := by
  have h := reciprocal_bounds n hn
  intro i
  cases i <;> simp only [means, Option.elim'] <;> constructor <;> linarith

theorem pair_gap (n : ℕ) (hn : 2 ≤ n) (i : Fin n) :
    hullGap (monomial (pairSupport i)) (means n) = 1 / n := by
  rw [monomial_hullGap_of_min_coordinate _ _ (means_mem_cube n hn) none
    (by simp [pairSupport])]
  · simp only [pairSupport, Finset.mem_singleton, reduceCtorEq, not_false_eq_true,
      Finset.sum_insert, Finset.sum_singleton, Finset.card_insert_of_notMem,
      Finset.card_singleton, means, Option.elim']
    norm_num
  · intro j hj
    simp only [pairSupport, Finset.mem_insert, Finset.mem_singleton] at hj
    rcases hj with rfl | rfl
    · exact le_rfl
    · have h := reciprocal_bounds n hn
      simp only [means, Option.elim']
      linarith

theorem leaf_gap (n : ℕ) (hn : 2 ≤ n) :
    hullGap (monomial (leafSupport n)) (means n) = 1 - 1 / n := by
  let i : Fin n := ⟨0, by omega⟩
  rw [monomial_hullGap_of_min_coordinate _ _ (means_mem_cube n hn) (some i)
    (mem_leafSupport i)]
  · have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
    have hs : ∑ j ∈ leafSupport n, means n j = (n : ℝ) - 1 := by
      rw [leafSupport, Finset.sum_image (fun _ _ _ _ h => Option.some.inj h)]
      simp only [means, Option.elim', Finset.sum_const, Finset.card_univ,
        Fintype.card_fin, nsmul_eq_mul]
      field_simp
    have hc : (leafSupport n).card = n := by
      rw [leafSupport, Finset.card_image_of_injective _ (Option.some_injective _)]
      simp
    rw [hs, hc]
    simp [means]
  · intro j hj
    obtain ⟨k, _, rfl⟩ := Finset.mem_image.mp hj
    exact le_rfl

theorem termwiseGap_eq (n : ℕ) (hn : 2 ≤ n) :
    termwiseGap (supports n) (means n) = 2 - 1 / n := by
  have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
  simp [termwiseGap, sum_supports, leaf_gap n hn, pair_gap n hn, hn0]
  ring


theorem polynomial_maximum (n : ℕ) (hn : 2 ≤ n) :
    IsGreatest (envelopeValues (polynomial n) (means n)) (2 - 1 / n) := by
  have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
  have hp (i : Fin n) : monomialUpper (pairSupport i) (means n) = 1 / n := by
    apply monomialUpper_eq_anchor _ _ none (by simp [pairSupport])
    intro j hj
    simp only [pairSupport, Finset.mem_insert, Finset.mem_singleton] at hj
    rcases hj with rfl | rfl
    · exact le_rfl
    · have h := reciprocal_bounds n hn
      simp only [means, Option.elim']
      linarith
  have hl : monomialUpper (leafSupport n) (means n) = 1 - 1 / n := by
    let i : Fin n := ⟨0, by omega⟩
    apply monomialUpper_eq_anchor _ _ (some i) (mem_leafSupport i)
    intro j hj
    obtain ⟨k, _, rfl⟩ := Finset.mem_image.mp hj
    exact le_rfl
  have h := positive_polynomial_maximum_general (supports n) (fun _ => 1)
    (by intros; norm_num) (means n) (means_mem_cube n hn)
  rw [supportPolynomial_eq] at h
  convert h using 1
  simp only [one_mul, sum_supports, hl, hp, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul]
  field_simp
  ring

/-- The affine lower bound valid at every binary vertex. -/
theorem polynomial_vertex_lower (n : ℕ) (v : Vertex (Coord n)) :
    (∑ i : Fin n, vertexPoint v (some i)) + ((n : ℝ) - 1) * vertexPoint v none
      - ((n : ℝ) - 1) ≤ polynomial n (vertexPoint v) := by
  have hnonneg : 0 ≤ ∏ i : Fin n, vertexPoint v (some i) := by
    apply Finset.prod_nonneg
    intro i _
    simp only [vertexPoint]
    split <;> norm_num
  have hlower := monomial_lower (Finset.univ : Finset (Fin n))
    (x := fun i => vertexPoint v (some i)) (by
      intro i _; simp only [vertexPoint]; split <;> norm_num)
  simp only [Finset.card_univ, Fintype.card_fin, monomial] at hlower
  simp only [vertexPoint] at hnonneg hlower
  cases h : v none <;> simp only [polynomial, vertexPoint, h, Bool.false_eq_true,
    if_false, if_true, mul_zero, mul_one, zero_mul, one_mul]
  · simpa only [add_zero, zero_add] using hlower
  · linarith

/-- Exactly one uniformly selected leaf fails; the anchor uses one selected atom. -/
def singleFailVertex (n : ℕ) (t : Fin n) : Vertex (Coord n) :=
  Option.elim' (decide (t.val = 0)) (fun i => decide (i ≠ t))

def singleFailLaw (n : ℕ) (hn : 0 < n) : Law (Vertex (Coord n)) := by
  letI : NeZero n := ⟨by omega⟩
  exact (Law.uniform (Fin n)).map (singleFailVertex n)

theorem singleFailLaw_expect (n : ℕ) (hn : 0 < n) (f : Vertex (Coord n) → ℝ) :
    (singleFailLaw n hn).expect f = (∑ t : Fin n, f (singleFailVertex n t)) / n := by
  let : NeZero n := ⟨by omega⟩
  simp [singleFailLaw, Law.expect_map, Law.expect_uniform, Function.comp_def]

theorem singleFail_vertex_sum (n : ℕ) (t : Fin n) :
    ∑ i : Fin n, vertexPoint (singleFailVertex n t) (some i) = (n : ℝ) - 1 := by
  simp only [singleFailVertex, vertexPoint, Option.elim', decide_eq_true_eq]
  rw [Finset.sum_ite, Finset.sum_const_zero, add_zero, Finset.sum_const,
    nsmul_eq_mul, mul_one]
  have hfilter : Finset.univ.filter (fun i : Fin n => i ≠ t) = Finset.univ.erase t := by
    ext i; simp
  rw [hfilter, Finset.card_erase_of_mem (Finset.mem_univ t), Finset.card_univ,
    Fintype.card_fin, Nat.cast_sub (by have := t.isLt; omega), Nat.cast_one]

theorem singleFail_vertex_prod (n : ℕ) (t : Fin n) :
    ∏ i : Fin n, vertexPoint (singleFailVertex n t) (some i) = 0 := by
  apply Finset.prod_eq_zero (Finset.mem_univ t)
  simp [vertexPoint, singleFailVertex]

theorem singleFailLaw_means (n : ℕ) (hn : 2 ≤ n) :
    HasMeans (singleFailLaw n (by omega)) (means n) := by
  have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
  intro i
  rw [singleFailLaw_expect]
  cases i with
  | none =>
      let z : Fin n := ⟨0, by omega⟩
      have hz : ∀ t : Fin n, t.val = 0 ↔ t = z := fun t => ⟨fun h => Fin.ext h,
        fun h => by rw [h]⟩
      simp [vertexPoint, singleFailVertex, means, hz]
  | some i =>
      have hs : (∑ t : Fin n, vertexPoint (singleFailVertex n t) (some i)) =
          (n : ℝ) - 1 := by
        convert singleFail_vertex_sum n i using 1
        apply Finset.sum_congr rfl
        intro t _
        simp [vertexPoint, singleFailVertex, ne_comm]
      rw [hs]
      simp only [means, Option.elim']
      field_simp

theorem polynomial_minimum (n : ℕ) (hn : 2 ≤ n) :
    IsLeast (envelopeValues (polynomial n) (means n)) (1 - 1 / n) := by
  have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast (show n ≠ 0 by omega)
  apply minimum_from_laws _ (polynomial_separatelyAffine n)
  · intro μ hm
    have hm' : ∀ i, μ.expect (fun v => vertexPoint v i) = means n i := hm
    have h := μ.expect_mono (polynomial_vertex_lower n)
    simp only [Law.expect_sub, Law.expect_add, Law.expect_sum, Law.expect_const_mul,
      Law.expect_const, hm', means, Option.elim', Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul] at h
    convert h using 1
    field_simp
    ring
  · refine ⟨singleFailLaw n (by omega), singleFailLaw_means n hn, ?_⟩
    have hv : ∀ t : Fin n, polynomial n (vertexPoint (singleFailVertex n t)) =
        ((n : ℝ) - 1) * vertexPoint (singleFailVertex n t) none := by
      intro t
      rw [polynomial, singleFail_vertex_sum, singleFail_vertex_prod]
      ring
    rw [singleFailLaw_expect, Finset.sum_congr rfl (fun t _ => hv t), ← Finset.mul_sum]
    have hmean := singleFailLaw_means n hn none
    rw [singleFailLaw_expect] at hmean
    change (∑ t : Fin n, vertexPoint (singleFailVertex n t) none) / n = 1 / n at hmean
    rw [mul_div_assoc, hmean]
    field_simp

theorem hullGap_eq (n : ℕ) (hn : 2 ≤ n) :
    hullGap (polynomial n) (means n) = 1 := by
  rw [hullGap, (polynomial_maximum n hn).csSup_eq, (polynomial_minimum n hn).csInf_eq]
  ring

theorem ratio_eq (n : ℕ) (hn : 2 ≤ n) :
    termwiseGap (supports n) (means n) / hullGap (polynomial n) (means n) =
      2 - 1 / n := by
  rw [termwiseGap_eq n hn, hullGap_eq n hn, div_one]


open Filter Topology

/-- The ratios of the actual graph-hull gaps converge to two. -/
theorem ratio_tendsto :
    Tendsto (fun n : ℕ => termwiseGap (supports n) (means n) /
      hullGap (polynomial n) (means n)) atTop (𝓝 2) := by
  have hi : Tendsto (fun n : ℕ => 1 / (n : ℝ)) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop tendsto_natCast_atTop_atTop
  have h : Tendsto (fun n : ℕ => 2 - 1 / (n : ℝ)) atTop (𝓝 2) := by
    simpa using tendsto_const_nhds.sub hi
  apply h.congr'
  filter_upwards [eventually_ge_atTop 2] with n hn
  exact (ratio_eq n hn).symm

/-- Any constant bounding all members of this family must be at least two. -/
theorem universal_constant_ge_two (C : ℝ)
    (hC : ∀ n : ℕ, 2 ≤ n → termwiseGap (supports n) (means n) ≤
      C * hullGap (polynomial n) (means n)) : 2 ≤ C := by
  apply le_of_tendsto ratio_tendsto
  filter_upwards [eventually_ge_atTop 2] with n hn
  simpa only [hullGap_eq n hn, mul_one, div_one] using hC n hn

end
end MultilinearGap.StructuralSharpness
