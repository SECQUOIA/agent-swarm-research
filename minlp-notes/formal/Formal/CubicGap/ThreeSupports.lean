import Formal.CubicGap.OrbitExpansion
import Formal.CubicGap.TermwiseFamilyUpper
import Formal.MultilinearGap.BoxSuprema

/-! Package the six three-group support orbits as one positive polynomial of degree at most three.
Repeated support contributions are added, so the representation uses distinct supports. -/
namespace CubicGap
open MultilinearGap
noncomputable section

/-- All possible supports of degree at most three on the three groups. Zero
coefficients are allowed; this avoids assumptions about the group size. -/
def threeSupports (m : ℕ) : Finset (Finset (Fin 3 × Fin m)) :=
  Finset.univ.filter (fun s => s.card ≤ 3)

theorem threeSupports_degree (m : ℕ) (s : Finset (Fin 3 × Fin m))
    (hs : s ∈ threeSupports m) : s.card ≤ 3 :=
  (Finset.mem_filter.mp hs).2

/-- Weighted evaluation of an arbitrary function on the six support orbits. -/
def threeOrbitSum (m : ℕ) (coef : Fin 6 → ℚ) :
    (Finset (Fin 3 × Fin m) → ℝ) →ₗ[ℝ] ℝ where
  toFun F :=
    (coef 0 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 3,
      F (s.map (groupEmbedding (2 : Fin 3)))) +
    (coef 1 : ℝ) * (∑ i : Fin m, ∑ s ∈ Finset.univ.powersetCard 2,
      F (insert (1,i) (s.map (groupEmbedding (2 : Fin 3))))) +
    (coef 2 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 2,
      F (s.map (groupEmbedding (1 : Fin 3)))) +
    (coef 3 : ℝ) * (∑ i : Fin m, ∑ j : Fin m, F {(0,i), (2,j)}) +
    (coef 4 : ℝ) * (∑ i : Fin m, ∑ j : Fin m, F {(0,i), (1,j)}) +
    (coef 5 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 2,
      F (s.map (groupEmbedding (0 : Fin 3))))
  map_add' F G := by simp [Finset.sum_add_distrib, mul_add]; ring
  map_smul' c F := by
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, ← Finset.mul_sum]
    ring

private theorem threeOrbitSum_congr_card (m : ℕ) (coef : Fin 6 → ℚ)
    (F G : Finset (Fin 3 × Fin m) → ℝ)
    (h : ∀ s, s.card = 2 ∨ s.card = 3 → F s = G s) :
    threeOrbitSum m coef F = threeOrbitSum m coef G := by
  have hg (g : Fin 3) (n : ℕ) (hn : n = 2 ∨ n = 3) (s : Finset (Fin m))
      (hs : s ∈ Finset.univ.powersetCard n) :
      F (s.map (groupEmbedding g)) = G (s.map (groupEmbedding g)) := by
    apply h
    simpa only [Finset.card_map, (Finset.mem_powersetCard.mp hs).2] using hn
  have hm (i : Fin m) (s : Finset (Fin m)) (hs : s ∈ Finset.univ.powersetCard 2) :
      F (insert (1,i) (s.map (groupEmbedding (2 : Fin 3)))) =
        G (insert (1,i) (s.map (groupEmbedding (2 : Fin 3)))) := by
    apply h
    right
    have hnot : (1, i) ∉ s.map (groupEmbedding (2 : Fin 3)) := by
      intro hmem
      obtain ⟨j, _, he⟩ := Finset.mem_map.mp hmem
      have hf := congrArg Prod.fst he
      change (2 : Fin 3) = 1 at hf
      exact (by decide : (2 : Fin 3) ≠ 1) hf
    rw [Finset.card_insert_of_notMem hnot, Finset.card_map,
      (Finset.mem_powersetCard.mp hs).2]
  have hc (g : Fin 3) (hg : g ≠ 0) (i j : Fin m) :
      F {(0,i),(g,j)} = G {(0,i),(g,j)} := by
    apply h
    left
    exact Finset.card_pair (fun he => hg (congrArg Prod.fst he).symm)
  have hgs (g : Fin 3) (n : ℕ) (hn : n = 2 ∨ n = 3) :=
    Finset.sum_congr rfl (hg g n hn)
  have hms (i : Fin m) := Finset.sum_congr rfl (hm i)
  have hcs (g : Fin 3) (hg : g ≠ 0) (i : Fin m) :=
    Finset.sum_congr (s₁ := Finset.univ) rfl (fun j _ => hc g hg i j)
  simp only [threeOrbitSum, LinearMap.coe_mk, AddHom.coe_mk,
    hgs 2 3 (by omega), hgs 1 2 (by omega), hgs 0 2 (by omega), hms,
    hcs 2 (by decide), hcs 1 (by decide)]

/-- The aggregate coefficient of each distinct support. -/
def threeSupportCoefficients (m : ℕ) (coef : Fin 6 → ℚ)
    (s : Finset (Fin 3 × Fin m)) : ℝ :=
  threeOrbitSum m coef (fun t => if t = s then 1 else 0)

private theorem threeOrbitSum_nonneg (m : ℕ) (coef : Fin 6 → ℚ)
    (hcoef : ∀ j, 0 ≤ coef j) (F : Finset (Fin 3 × Fin m) → ℝ)
    (hF : ∀ s, 0 ≤ F s) : 0 ≤ threeOrbitSum m coef F := by
  have hcoef' (j) : 0 ≤ (coef j : ℝ) := by exact_mod_cast hcoef j
  dsimp only [threeOrbitSum, LinearMap.coe_mk, AddHom.coe_mk]
  repeat' first
    | apply add_nonneg
    | apply mul_nonneg (hcoef' _)
    | apply Finset.sum_nonneg; intro s hs
    | exact hF _

theorem threeSupportCoefficients_nonneg (m : ℕ) (coef : Fin 6 → ℚ)
    (hcoef : ∀ j, 0 ≤ coef j) (s : Finset (Fin 3 × Fin m)) :
    0 ≤ threeSupportCoefficients m coef s := by
  apply threeOrbitSum_nonneg m coef hcoef
  intro t
  split <;> norm_num

/-- A nonzero coefficient belongs to a quadratic or cubic support. -/
theorem threeSupportCoefficients_card (m : ℕ) (coef : Fin 6 → ℚ)
    (s : Finset (Fin 3 × Fin m)) (hs : threeSupportCoefficients m coef s ≠ 0) :
    s.card = 2 ∨ s.card = 3 := by
  by_contra hn
  apply hs
  calc
    _ = threeOrbitSum m coef 0 := by
      apply threeOrbitSum_congr_card
      intro t ht
      have hne : t ≠ s := by intro he; subst t; exact hn ht
      simp [hne]
    _ = 0 := map_zero _

private theorem natValued_add {a b : ℝ} (ha : ∃ n : ℕ, a = n)
    (hb : ∃ n : ℕ, b = n) : ∃ n : ℕ, a + b = n := by
  obtain ⟨n, rfl⟩ := ha
  obtain ⟨k, rfl⟩ := hb
  exact ⟨n + k, (Nat.cast_add _ _).symm⟩

private theorem natValued_mul {a b : ℝ} (ha : ∃ n : ℕ, a = n)
    (hb : ∃ n : ℕ, b = n) : ∃ n : ℕ, a * b = n := by
  obtain ⟨n, rfl⟩ := ha
  obtain ⟨k, rfl⟩ := hb
  exact ⟨n * k, (Nat.cast_mul _ _).symm⟩

private theorem natValued_sum {J : Type*} (S : Finset J) (f : J → ℝ)
    (hf : ∀ j ∈ S, ∃ n : ℕ, f j = n) : ∃ n : ℕ, ∑ j ∈ S, f j = n := by
  classical
  induction S using Finset.induction_on with
  | empty => exact ⟨0, by simp⟩
  | @insert j S hj ih =>
    rw [Finset.sum_insert hj]
    exact natValued_add (hf j (by simp)) (ih (fun k hk => hf k (by simp [hk])))

/-- Natural orbit coefficients remain natural after equal supports are collected. -/
theorem threeSupportCoefficients_nat (m : ℕ) (coef : Fin 6 → ℚ)
    (hcoef : ∀ j, ∃ n : ℕ, coef j = (n : ℚ))
    (s : Finset (Fin 3 × Fin m)) :
    ∃ n : ℕ, threeSupportCoefficients m coef s = (n : ℝ) := by
  have hcoef' (j) : ∃ n : ℕ, (coef j : ℝ) = n := by
    obtain ⟨n, hn⟩ := hcoef j
    exact ⟨n, by rw [hn]; norm_cast⟩
  have hdelta (t : Finset (Fin 3 × Fin m)) :
      ∃ n : ℕ, (if t = s then (1 : ℝ) else 0) = n := by
    by_cases h : t = s
    · exact ⟨1, by simp [h]⟩
    · exact ⟨0, by simp [h]⟩
  dsimp only [threeSupportCoefficients, threeOrbitSum, LinearMap.coe_mk, AddHom.coe_mk]
  repeat' first
    | apply natValued_add
    | apply natValued_mul (hcoef' _)
    | apply natValued_sum; intro t ht
    | exact hdelta _

/-- Collecting equal supports preserves every linear sum of their values. -/
theorem threeSupportCoefficients_sum (m : ℕ) (coef : Fin 6 → ℚ)
    (F : Finset (Fin 3 × Fin m) → ℝ) :
    (∑ s ∈ threeSupports m, threeSupportCoefficients m coef s * F s) =
      threeOrbitSum m coef F := by
  calc
    _ = threeOrbitSum m coef (∑ s ∈ threeSupports m,
        F s • (fun t => if t = s then (1 : ℝ) else 0)) := by
      simp only [map_sum, map_smul, smul_eq_mul, threeSupportCoefficients]
      apply Finset.sum_congr rfl
      intro s _
      ring
    _ = threeOrbitSum m coef F := by
      apply threeOrbitSum_congr_card
      intro s hs
      have hs : s.card ≤ 3 := by omega
      have hmem : s ∈ threeSupports m := by simp [threeSupports, hs]
      simp [Finset.sum_apply, hmem]

theorem threeFamily_eq_supportPolynomial (m : ℕ) (coef : Fin 6 → ℚ) :
    threeFamily m coef = supportPolynomial (threeSupports m) (threeSupportCoefficients m coef) := by
  funext x
  rw [supportPolynomial, threeSupportCoefficients_sum]
  exact threeFamily_orbit_expansion m coef x

theorem threeTermwiseGap_eq_weightedTermwiseGap (m : ℕ) (coef : Fin 6 → ℚ) :
    termwiseUpperThree m coef - termwiseLowerThree m coef =
      weightedTermwiseGap (threeSupports m) (threeSupportCoefficients m coef)
        (thresholdThreeMeans m) := by
  rw [weightedTermwiseGap, threeSupportCoefficients_sum]
  change threeOrbitSum m coef (fun s => factorUpper s (thresholdThreeMeans m)) -
    threeOrbitSum m coef (fun s => factorLower s (thresholdThreeMeans m)) = _
  rw [← map_sub]
  rfl

theorem three_ratio_mem_degreeRatios (m : ℕ) (coef : Fin 6 → ℚ)
    (hcoef : ∀ j, 0 ≤ coef j)
    (hpos : 0 < hullGap (threeFamily m coef) (thresholdThreeMeans m)) :
    (termwiseUpperThree m coef - termwiseLowerThree m coef) /
      hullGap (threeFamily m coef) (thresholdThreeMeans m) ∈ degreeRatios 3 := by
  refine ⟨Fin 3 × Fin m, inferInstance, inferInstance, threeSupports m,
    threeSupportCoefficients m coef, thresholdThreeMeans m,
    fun s _ => threeSupportCoefficients_nonneg m coef hcoef s,
    threeSupports_degree m, thresholdThreeMeans_mem_cube m, ?_, ?_⟩
  · simpa only [← threeFamily_eq_supportPolynomial] using hpos
  · rw [← threeFamily_eq_supportPolynomial, ← threeTermwiseGap_eq_weightedTermwiseGap]

theorem three_ratio_mem_boxDegreeRatios (m : ℕ) (coef : Fin 6 → ℚ)
    (hcoef : ∀ j, 0 ≤ coef j)
    (hpos : 0 < hullGap (threeFamily m coef) (thresholdThreeMeans m)) :
    (termwiseUpperThree m coef - termwiseLowerThree m coef) /
      hullGap (threeFamily m coef) (thresholdThreeMeans m) ∈ boxDegreeRatios 3 :=
  degreeRatios_subset_boxDegreeRatios 3 (three_ratio_mem_degreeRatios m coef hcoef hpos)

end
end CubicGap
