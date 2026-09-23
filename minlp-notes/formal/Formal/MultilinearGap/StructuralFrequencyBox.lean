import Formal.MultilinearGap.BilinearGraph

/-! # Support-preserving box normalization

Zero-lower boxes rescale coefficients without expanding the support family.
The transfer theorem below assumes a cube bound; it does not prove the
frequency-two gap theorem. Common-aspect positive boxes retain each original
factor as a convex exponential cardinality sequence. The final section proves
the exact unequal-aspect positive-box obstruction from
`notes/multilinear-frequency-two-positive-box-obstruction.md`: the original
termwise gap is `7/4`, the full hull gap is `3/2`, and their ratio is `7/6`.
All envelope endpoints are certified by affine bounds on all eight vertices
and attaining finite probability laws. -/

namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- Coefficients after coordinatewise scaling. The support family is unchanged. -/
def zeroLowerCoefficient (u : I → ℝ) (a : Finset I → ℝ) (s : Finset I) : ℝ :=
  a s * ∏ i ∈ s, u i

omit [Fintype I] [DecidableEq I] in
theorem zeroLowerCoefficient_nonneg (u : I → ℝ) (hu : ∀ i, 0 ≤ u i)
    (a : Finset I → ℝ) (s : Finset I) (ha : 0 ≤ a s) :
    0 ≤ zeroLowerCoefficient u a s :=
  mul_nonneg ha (Finset.prod_nonneg fun i _ => hu i)

omit [Fintype I] [DecidableEq I] in
/-- At zero lower bounds a monomial remains one monomial, even if a side is zero. -/
theorem monomial_zeroLower (u p : I → ℝ) (s : Finset I) :
    monomial s (boxPoint (fun _ => 0) u p) =
      (∏ i ∈ s, u i) * monomial s p := by
  simp [monomial, boxPoint, Finset.prod_mul_distrib]

omit [Fintype I] [DecidableEq I] in
theorem supportPolynomial_zeroLower (S : Finset (Finset I)) (a : Finset I → ℝ)
    (u p : I → ℝ) :
    supportPolynomial S a (boxPoint (fun _ => 0) u p) =
      supportPolynomial S (zeroLowerCoefficient u a) p := by
  unfold supportPolynomial zeroLowerCoefficient
  apply Finset.sum_congr rfl
  intro s _
  rw [monomial_zeroLower]
  ring

/-- Exact full-hull transfer; it does not require positive coefficients. -/
theorem boxHullGap_zeroLower (S : Finset (Finset I)) (a : Finset I → ℝ)
    (u : I → ℝ) (hu : ∀ i, 0 ≤ u i) (p : I → ℝ) (hp : p ∈ cube I) :
    boxHullGap (fun _ => 0) u (supportPolynomial S a) (boxPoint (fun _ => 0) u p) =
      hullGap (supportPolynomial S (zeroLowerCoefficient u a)) p := by
  rw [boxHullGap_eq_of_mem _ _ hu _ p hp]
  congr 1
  funext q
  exact supportPolynomial_zeroLower S a u q

/-- Exact termwise transfer, using the original support family throughout. -/
theorem boxTermwiseGap_zeroLower (S : Finset (Finset I)) (a : Finset I → ℝ)
    (u : I → ℝ) (hu : ∀ i, 0 ≤ u i) (p : I → ℝ) (hp : p ∈ cube I) :
    boxTermwiseGap S a (fun _ => 0) u (boxPoint (fun _ => 0) u p) =
      weightedTermwiseGap S (zeroLowerCoefficient u a) p := by
  unfold boxTermwiseGap weightedTermwiseGap zeroLowerCoefficient
  apply Finset.sum_congr rfl
  intro s _
  rw [boxHullGap_eq_of_mem _ _ hu _ p hp]
  have he : (fun q => monomial s (boxPoint (fun _ => 0) u q)) =
      (fun q => (∏ i ∈ s, u i) * monomial s q) := by
    funext q
    exact monomial_zeroLower u q s
  rw [he, hullGap_monomial_scale s p hp _ (Finset.prod_nonneg fun i _ => hu i)]
  ring

/-- Any bound valid for nonnegative coefficients on a fixed support family
transfers to every zero-lower box. Thus incidence restrictions are preserved
without requiring a theorem about expanded monomial supports. -/
theorem zeroLower_gap_bound_transfer (S : Finset (Finset I)) (C : ℝ)
    (hbound : ∀ (b : Finset I → ℝ), (∀ s ∈ S, 0 ≤ b s) →
      ∀ p ∈ cube I, weightedTermwiseGap S b p ≤ C * hullGap (supportPolynomial S b) p)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (u : I → ℝ) (hu : ∀ i, 0 ≤ u i)
    (x : I → ℝ) (hx : x ∈ coordinateBox (fun _ => 0) u) :
    boxTermwiseGap S a (fun _ => 0) u x ≤
      C * boxHullGap (fun _ => 0) u (supportPolynomial S a) x := by
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint _ _ hu x hx
  rw [boxTermwiseGap_zeroLower S a u hu p hp, boxHullGap_zeroLower S a u hu p hp]
  exact hbound _ (fun s hs => zeroLowerCoefficient_nonneg u hu a s (ha s hs)) p hp

/-- A weighted positive-box factor's cardinality sequence. -/
def commonAspectSequence (rho : ℝ) (l : I → ℝ) (a : ℝ) (s : Finset I) (k : ℕ) : ℝ :=
  a * (∏ i ∈ s, l i) * rho ^ k

omit [Fintype I] [DecidableEq I] in
/-- Common-aspect normalization retains each factor's original support. -/
theorem monomial_commonAspect_vertex (rho : ℝ) (l : I → ℝ) (a : ℝ)
    (s : Finset I) (v : Vertex I) :
    a * monomial s (boxPoint l (fun i => rho * l i) (vertexPoint v)) =
      commonAspectSequence rho l a s (boxSuccessCount s v) := by
  have he : boxPoint l (fun i => rho * l i) (vertexPoint v) =
      fun i => l i * boxPoint (fun _ => 1) (fun _ => rho) (vertexPoint v) i := by
    funext i
    simp only [boxPoint]
    ring
  rw [he]
  simp only [monomial, Finset.prod_mul_distrib]
  change a * ((∏ i ∈ s, l i) * monomial s
    (boxPoint (fun _ => 1) (fun _ => rho) (vertexPoint v))) = _
  rw [monomial_boxPoint_vertex_pow]
  unfold commonAspectSequence
  ring

omit [Fintype I] [DecidableEq I] in
/-- The exponential cardinality sequence is discretely convex, including
zero coefficients and the degenerate common aspect ratio one. -/
theorem commonAspectSequence_convex (rho : ℝ) (hrho : 0 ≤ rho)
    (l : I → ℝ) (hl : ∀ i, 0 ≤ l i) (a : ℝ) (ha : 0 ≤ a)
    (s : Finset I) (k : ℕ) :
    0 ≤ commonAspectSequence rho l a s (k + 2) -
      2 * commonAspectSequence rho l a s (k + 1) + commonAspectSequence rho l a s k := by
  have hn : 0 ≤ a * (∏ i ∈ s, l i) * rho ^ k * (rho - 1) ^ 2 :=
    mul_nonneg (mul_nonneg (mul_nonneg ha (Finset.prod_nonneg fun i _ => hl i))
      (pow_nonneg hrho k)) (sq_nonneg _)
  unfold commonAspectSequence
  simp only [pow_add, pow_one, pow_two]
  nlinarith

namespace PositiveBoxObstruction

attribute [local simp] Matrix.cons_val_two Matrix.cons_val_three Matrix.vecHead Matrix.vecTail

/-- The unequal-aspect box from the exact positive-box obstruction. -/
def lower : Fin 3 → ℝ := ![1, 1, 1]
def upper : Fin 3 → ℝ := ![2, 2, 3]
def means : Fin 3 → ℝ := ![1/4, 1/4, 3/4]
def pair : Finset (Fin 3) := {0, 1}
def triple : Finset (Fin 3) := Finset.univ
def supports : Finset (Finset (Fin 3)) := {pair, triple}

def normalized (s : Finset (Fin 3)) (p : Fin 3 → ℝ) : ℝ :=
  monomial s (boxPoint lower upper p)

private theorem normalized_pair (p : Fin 3 → ℝ) :
    normalized pair p = (1 + p 0) * (1 + p 1) := by
  norm_num [normalized, pair, monomial, boxPoint, lower, upper]

private theorem normalized_triple (p : Fin 3 → ℝ) :
    normalized triple p = (1 + p 0) * (1 + p 1) * (1 + 2 * p 2) := by
  simp [normalized, triple, monomial, boxPoint, lower, upper, Fin.prod_univ_succ]
  ring

private def quarterLaw (v : Fin 4 → Vertex (Fin 3)) : Law (Vertex (Fin 3)) :=
  (Law.uniform (Fin 4)).map v

private theorem quarterLaw_expect (v : Fin 4 → Vertex (Fin 3))
    (f : Vertex (Fin 3) → ℝ) :
    (quarterLaw v).expect f = (f (v 0) + f (v 1) + f (v 2) + f (v 3)) / 4 := by
  simp [quarterLaw, Law.expect_uniform, Fin.sum_univ_succ]
  ring

private def lowerPairStates : Fin 4 → Vertex (Fin 3) :=
  ![![false,false,false], ![false,false,true], ![false,true,true], ![true,false,true]]
private def lowerTripleStates : Fin 4 → Vertex (Fin 3) :=
  ![![false,false,true], ![false,false,true], ![false,false,true], ![true,true,false]]
private def lowerSumStates : Fin 4 → Vertex (Fin 3) :=
  ![![false,false,true], ![false,false,true], ![false,true,true], ![true,false,false]]
private def upperStates : Fin 4 → Vertex (Fin 3) :=
  ![![false,false,false], ![false,false,true], ![false,false,true], ![true,true,true]]

private theorem states_means (v : Fin 4 → Vertex (Fin 3))
    (hv : v = lowerPairStates ∨ v = lowerTripleStates ∨ v = lowerSumStates ∨ v = upperStates) :
    HasMeans (quarterLaw v) means := by
  rcases hv with rfl | rfl | rfl | rfl <;>
    intro i <;> fin_cases i <;>
    norm_num [quarterLaw_expect, lowerPairStates, lowerTripleStates, lowerSumStates,
      upperStates, vertexPoint, means]

private def affineValue (c : Fin 4 → ℝ) (p : Fin 3 → ℝ) : ℝ :=
  c 0 + c 1 * p 0 + c 2 * p 1 + c 3 * p 2

private theorem affineValue_expect (c : Fin 4 → ℝ) (μ : Law (Vertex (Fin 3)))
    (hm : HasMeans μ means) :
    μ.expect (fun v => affineValue c (vertexPoint v)) = affineValue c means := by
  change ∀ i, _ = _ at hm
  simp only [affineValue, Law.expect_add, Law.expect_const, Law.expect_const_mul, hm]

private theorem certificate (f : (Fin 3 → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (lo hi : Fin 4 → ℝ) (L U : ℝ)
    (lb : ∀ v : Vertex (Fin 3), affineValue lo (vertexPoint v) ≤ f (vertexPoint v))
    (ub : ∀ v : Vertex (Fin 3), f (vertexPoint v) ≤ affineValue hi (vertexPoint v))
    (lv : affineValue lo means = L) (uv : affineValue hi means = U)
    (vl vu : Fin 4 → Vertex (Fin 3))
    (ml : HasMeans (quarterLaw vl) means) (mu : HasMeans (quarterLaw vu) means)
    (al : (quarterLaw vl).expect (fun v => f (vertexPoint v)) = L)
    (au : (quarterLaw vu).expect (fun v => f (vertexPoint v)) = U) :
    hullGap f means = U - L := by
  have hmin := minimum_from_laws f hf means L (fun μ hm => by
    have h := μ.expect_mono lb
    rw [affineValue_expect lo μ hm, lv] at h
    exact h) ⟨quarterLaw vl, ml, al⟩
  have hmax := maximum_from_laws f hf means U (fun μ hm => by
    have h := μ.expect_mono ub
    rw [affineValue_expect hi μ hm, uv] at h
    exact h) ⟨quarterLaw vu, mu, au⟩
  rw [hullGap, hmin.csInf_eq, hmax.csSup_eq]

/-- The `xy` factor has exact gap `1/4` at the normalized obstruction point. -/
theorem pair_gap : hullGap (normalized pair) means = 1/4 := by
  have he := certificate (normalized pair) (separatelyAffine_box_monomial lower upper pair)
    ![1,1,1,0] ![1,2,1,0] (3/2) (7/4)
    (by intro v; cases h0 : v 0 <;> cases h1 : v 1 <;> cases h2 : v 2 <;>
        norm_num [affineValue, normalized_pair, vertexPoint, h0, h1, h2])
    (by intro v; cases h0 : v 0 <;> cases h1 : v 1 <;> cases h2 : v 2 <;>
        norm_num [affineValue, normalized_pair, vertexPoint, h0, h1, h2])
    (by norm_num [affineValue, means]) (by norm_num [affineValue, means])
    lowerPairStates upperStates
    (states_means _ (Or.inl rfl)) (states_means _ (Or.inr (Or.inr (Or.inr rfl))))
    (by norm_num [quarterLaw_expect, lowerPairStates, normalized_pair, vertexPoint])
    (by norm_num [quarterLaw_expect, upperStates, normalized_pair, vertexPoint])
  norm_num at he ⊢
  exact he

/-- The `xyz` factor has exact gap `3/2` at the obstruction point. -/
theorem triple_gap : hullGap (normalized triple) means = 3/2 := by
  have he := certificate (normalized triple) (separatelyAffine_box_monomial lower upper triple)
    ![0,2,2,3] ![1,6,3,2] (13/4) (19/4)
    (by intro v; cases h0 : v 0 <;> cases h1 : v 1 <;> cases h2 : v 2 <;>
        norm_num [affineValue, normalized_triple, vertexPoint, h0, h1, h2])
    (by intro v; cases h0 : v 0 <;> cases h1 : v 1 <;> cases h2 : v 2 <;>
        norm_num [affineValue, normalized_triple, vertexPoint, h0, h1, h2])
    (by norm_num [affineValue, means]) (by norm_num [affineValue, means])
    lowerTripleStates upperStates
    (states_means _ (Or.inr (Or.inl rfl))) (states_means _ (Or.inr (Or.inr (Or.inr rfl))))
    (by norm_num [quarterLaw_expect, lowerTripleStates, normalized_triple, vertexPoint])
    (by norm_num [quarterLaw_expect, upperStates, normalized_triple, vertexPoint])
  norm_num at he ⊢
  exact he

private theorem pair_ne_triple : pair ≠ triple := by decide

private theorem normalized_sum (p : Fin 3 → ℝ) :
    supportPolynomial supports (fun _ => 1) (boxPoint lower upper p) =
      normalized pair p + normalized triple p := by
  simp [supportPolynomial, supports, pair_ne_triple, normalized]

/-- The sum's exact hull gap is `3/2`, strictly below the sum of local gaps. -/
theorem sum_gap : hullGap (fun p => normalized pair p + normalized triple p) means = 3/2 := by
  have hf : SeparatelyAffine (fun p => normalized pair p + normalized triple p) := by
    have h := separatelyAffine_boxPoint _
      (supportPolynomial_coordinate_affine supports (fun _ => (1 : ℝ))) lower upper
    simpa only [normalized_sum] using h
  have he := certificate _ hf ![0,4,4,4] ![2,8,4,2] 5 (13/2)
    (by intro v; cases h0 : v 0 <;> cases h1 : v 1 <;> cases h2 : v 2 <;>
        norm_num [affineValue, normalized_pair, normalized_triple, vertexPoint, h0, h1, h2])
    (by intro v; cases h0 : v 0 <;> cases h1 : v 1 <;> cases h2 : v 2 <;>
        norm_num [affineValue, normalized_pair, normalized_triple, vertexPoint, h0, h1, h2])
    (by norm_num [affineValue, means]) (by norm_num [affineValue, means])
    lowerSumStates upperStates
    (states_means _ (Or.inr (Or.inr (Or.inl rfl))))
    (states_means _ (Or.inr (Or.inr (Or.inr rfl))))
    (by norm_num [quarterLaw_expect, lowerSumStates, normalized_pair,
      normalized_triple, vertexPoint])
    (by norm_num [quarterLaw_expect, upperStates, normalized_pair, normalized_triple, vertexPoint])
  norm_num at he ⊢
  exact he

private theorem ordered_box : ∀ i, lower i ≤ upper i := by
  intro i; fin_cases i <;> norm_num [lower, upper]
private theorem means_mem : means ∈ cube (Fin 3) := by
  intro i; fin_cases i <;> norm_num [means]

/-- Exact original-box termwise and full-hull gaps for `xy + xyz` at
`(5/4, 5/4, 5/2)`, with no floating point calculations. -/
theorem original_box_gaps :
    boxTermwiseGap supports (fun _ => 1) lower upper ![5/4, 5/4, 5/2] = 7/4 ∧
    boxHullGap lower upper (supportPolynomial supports (fun _ => 1))
      ![5/4, 5/4, 5/2] = 3/2 := by
  have hp : boxPoint lower upper means = ![5/4, 5/4, 5/2] := by
    funext i; fin_cases i <;> norm_num [boxPoint, lower, upper, means]
  rw [← hp]
  constructor
  · simp only [boxTermwiseGap, supports, Finset.sum_insert,
      Finset.mem_singleton, pair_ne_triple, not_false_eq_true, Finset.sum_singleton, one_mul]
    rw [boxHullGap_eq_of_mem lower upper ordered_box _ means means_mem,
      boxHullGap_eq_of_mem lower upper ordered_box _ means means_mem]
    change hullGap (normalized pair) means + hullGap (normalized triple) means = _
    rw [pair_gap, triple_gap]
    norm_num
  · rw [boxHullGap_eq_of_mem lower upper ordered_box _ means means_mem]
    simpa only [normalized_sum] using sum_gap

/-- The positive-box obstruction ratio is exactly `7/6`. -/
theorem original_box_ratio :
    boxTermwiseGap supports (fun _ => 1) lower upper ![5/4, 5/4, 5/2] /
      boxHullGap lower upper (supportPolynomial supports (fun _ => 1))
        ![5/4, 5/4, 5/2] = 7/6 := by
  rw [original_box_gaps.1, original_box_gaps.2]
  norm_num

/-- The witness is a strictly positive box with a feasible evaluation point. -/
theorem positive_box_data :
    (∀ i, 0 < lower i ∧ lower i < upper i) ∧
    ![5/4, 5/4, 5/2] ∈ coordinateBox lower upper := by
  constructor
  · intro i; fin_cases i <;> norm_num [lower, upper]
  · intro i; fin_cases i <;> norm_num [lower, upper]

/-- The original factorwise relaxation is strictly wider than the scalar hull. -/
theorem original_box_strict_gap :
    boxHullGap lower upper (supportPolynomial supports (fun _ => 1))
        ![5/4, 5/4, 5/2] <
      boxTermwiseGap supports (fun _ => 1) lower upper ![5/4, 5/4, 5/2] := by
  rw [original_box_gaps.1, original_box_gaps.2]
  norm_num

/-- Every coordinate of this witness occurs in at most two original factors. -/
theorem support_frequency_two (i : Fin 3) :
    (supports.filter fun s => i ∈ s).card ≤ 2 := by
  fin_cases i <;> decide

/-- An explicit proper two-coloring of the original factors. Shared
coordinates join the two opposite colors; the private coordinate can be
attached to a dummy factor of the opposite color. -/
theorem factor_two_coloring : ∃ color : Finset (Fin 3) → Bool,
    ∀ s ∈ supports, ∀ t ∈ supports, s ≠ t →
      ∀ i : Fin 3, i ∈ s → i ∈ t → color s ≠ color t := by
  refine ⟨fun s => decide (s = pair), ?_⟩
  intro s hs t ht hne i his hit
  simp only [supports, Finset.mem_insert, Finset.mem_singleton] at hs ht
  rcases hs with rfl | rfl <;> rcases ht with rfl | rfl
  · exact False.elim (hne rfl)
  · simp [pair_ne_triple.symm]
  · simp [pair_ne_triple.symm]
  · exact False.elim (hne rfl)

end PositiveBoxObstruction
end
end MultilinearGap
