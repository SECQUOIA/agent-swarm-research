import Formal.CubicGap.TermwiseUpper

/-! Exact lower envelopes of arbitrary squarefree monomials, with all ambient
coordinate means preserved by an attaining finite binary law. -/
namespace MultilinearGap
open CubicGap
noncomputable section

private theorem binary_coupling (p a : ℝ) (hp : 0 ≤ p ∧ p ≤ 1)
    (ha : 0 ≤ a ∧ a ≤ 1) :
    ∃ q₀ q₁ : ℝ, (0 ≤ q₀ ∧ q₀ ≤ 1) ∧ (0 ≤ q₁ ∧ q₁ ≤ 1) ∧
      (1-p)*q₀+p*q₁ = a ∧ p*q₁ = max 0 (p+a-1) := by
  by_cases hp0 : p = 0
  · subst p
    refine ⟨a, 0, ha, by norm_num, by ring, ?_⟩
    rw [max_eq_left (by linarith)]
    ring
  by_cases hp1 : p = 1
  · subst p
    refine ⟨0, a, by norm_num, ha, by ring, ?_⟩
    rw [max_eq_right (by linarith)]
    ring
  by_cases hpa : p+a ≤ 1
  · have hd : 0 < 1-p := by
      have : p < 1 := lt_of_le_of_ne hp.2 hp1
      linarith
    refine ⟨a/(1-p), 0, ⟨div_nonneg ha.1 hd.le, (div_le_one hd).mpr (by linarith)⟩,
      by norm_num, ?_, ?_⟩
    · field_simp; ring
    · rw [max_eq_left (by linarith)]; ring
  · have hp' : 0 < p := lt_of_le_of_ne hp.1 (Ne.symm hp0)
    refine ⟨1, (p+a-1)/p, by norm_num,
      ⟨div_nonneg (by linarith) hp.1, (div_le_one hp').mpr (by linarith)⟩, ?_, ?_⟩
    · field_simp; ring
    · rw [max_eq_right (by linarith)]
      field_simp

variable {I : Type*} [Fintype I] [DecidableEq I]

private def splitLaw (μ : Law (Vertex I)) (q : Vertex I → ℝ)
    (hq : ∀ v, 0 ≤ q v ∧ q v ≤ 1) : Law (Vertex I × Bool) where
  weight t := μ.weight t.1 * (if t.2 then q t.1 else 1-q t.1)
  nonneg t := mul_nonneg (μ.nonneg _) (by
    cases t.2
    · exact sub_nonneg.mpr (hq _).2
    · exact (hq _).1)
  mass_one := by
    simp only [Fintype.sum_prod_type, Fintype.sum_bool]
    convert μ.mass_one using 1
    apply Finset.sum_congr rfl
    intro v _
    simp
    ring

private theorem splitLaw_expect (μ : Law (Vertex I)) (q : Vertex I → ℝ)
    (hq : ∀ v, 0 ≤ q v ∧ q v ≤ 1) (f : Vertex I × Bool → ℝ) :
    (splitLaw μ q hq).expect f =
      μ.expect (fun v => (1-q v)*f (v,false)+q v*f (v,true)) := by
  simp only [Law.expect, splitLaw, Fintype.sum_prod_type, Fintype.sum_bool]
  apply Finset.sum_congr rfl
  intro v _
  simp
  ring

omit [Fintype I] [DecidableEq I] in
private theorem monomial_binary (s : Finset I) (v : Vertex I) :
    monomial s (vertexPoint v) = 0 ∨ monomial s (vertexPoint v) = 1 := by
  by_cases h : ∃ i ∈ s, v i = false
  · obtain ⟨i, hi, hv⟩ := h
    exact Or.inl (Finset.prod_eq_zero hi (by simp [vertexPoint, hv]))
  · right
    apply Finset.prod_eq_one
    intro i hi
    have hv : v i = true := by cases hv : v i <;> simp_all
    simp [vertexPoint, hv]

/-- Every squarefree monomial attains the Fréchet lower bound in a finite binary
law that preserves every coordinate mean, including coordinates outside its support. -/
theorem monomial_lower_attaining_law (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧
      μ.expect (fun v => monomial s (vertexPoint v)) =
        max 0 ((∑ i ∈ s, x i) - (s.card - 1 : ℝ)) := by
  induction s using Finset.induction_on with
  | empty =>
    have h := (mem_cubeGraph_hull_iff (monomial (∅ : Finset I))
      (monomial_coordinate_affine ∅) x 1).mp
      (by exact subset_convexHull ℝ _ ⟨hx, by simp [monomial]⟩)
    simpa [HasMeans] using h
  | @insert a s ha ih =>
    obtain ⟨μ, hmean, hvalue⟩ := ih
    let M := fun v : Vertex I => monomial s (vertexPoint v)
    let p := μ.expect M
    have hp : 0 ≤ p ∧ p ≤ 1 := by
      refine ⟨monomial_expect_nonneg s μ, ?_⟩
      calc p ≤ μ.expect (fun _ => 1) := μ.expect_mono (fun v => by
             rcases monomial_binary s v with h | h <;> simp [M, h])
           _ = 1 := μ.expect_const 1
    obtain ⟨q₀, q₁, hq₀, hq₁, hqa, hqp⟩ := binary_coupling p (x a) hp (hx a)
    let q := fun v => q₀ + (q₁-q₀)*M v
    have hq : ∀ v, 0 ≤ q v ∧ q v ≤ 1 := by
      intro v
      rcases monomial_binary s v with h | h
      · simpa [q, M, h] using hq₀
      · simpa [q, M, h] using hq₁
    let ν := (splitLaw μ q hq).map (fun t => Function.update t.1 a t.2)
    have hqmean : μ.expect q = x a := by
      dsimp [q]
      rw [μ.expect_add, μ.expect_const, μ.expect_const_mul]
      change q₀ + (q₁-q₀)*p = x a
      linarith [hqa]
    have hνmean : HasMeans ν x := by
      intro i
      change ((splitLaw μ q hq).map _).expect _ = _
      rw [Law.expect_map, splitLaw_expect]
      by_cases hi : i = a
      · subst i
        simpa [Function.comp_def, vertexPoint] using hqmean
      · have heq : (fun v : Vertex I =>
            (1-q v)*vertexPoint (Function.update v a false) i +
            q v*vertexPoint (Function.update v a true) i) =
            fun v => vertexPoint v i := by
          funext v
          simp only [vertexPoint, Function.update_of_ne hi]
          ring
        change μ.expect (fun v => (1-q v)*vertexPoint (Function.update v a false) i +
          q v*vertexPoint (Function.update v a true) i) = x i
        rw [heq]
        exact hmean i
    have hνvalue : ν.expect (fun v => monomial (insert a s) (vertexPoint v)) =
        max 0 (p+x a-1) := by
      change ((splitLaw μ q hq).map _).expect _ = _
      rw [Law.expect_map, splitLaw_expect]
      have hpoint (v : Vertex I) (b : Bool) :
          monomial (insert a s) (vertexPoint (Function.update v a b)) =
          (if b then 1 else 0) * M v := by
        rw [monomial, Finset.prod_insert ha]
        congr 1
        · simp [vertexPoint]
        · apply Finset.prod_congr rfl
          intro i hi
          have hia : i ≠ a := by intro he; subst i; contradiction
          simp [vertexPoint, Function.update_of_ne hia]
      change μ.expect (fun v =>
        (1-q v)*monomial (insert a s) (vertexPoint (Function.update v a false)) +
        q v*monomial (insert a s) (vertexPoint (Function.update v a true))) = _
      simp_rw [hpoint]
      simp only [Bool.false_eq_true, if_false, zero_mul, mul_zero,
        if_true, one_mul, zero_add]
      have heq : (fun v => q v * M v) = fun v => q₁ * M v := by
        funext v
        rcases monomial_binary s v with h | h <;> simp [q, M, h]
      rw [heq, μ.expect_const_mul]
      exact (mul_comm q₁ p).trans hqp
    refine ⟨ν, hνmean, hνvalue.trans ?_⟩
    rw [Finset.sum_insert ha, Finset.card_insert_of_notMem ha, Nat.cast_add, Nat.cast_one]
    have hpvalue : p = max 0 ((∑ i ∈ s, x i) - (s.card - 1 : ℝ)) := hvalue
    rw [hpvalue]
    rcases le_total ((∑ i ∈ s, x i) - (s.card - 1 : ℝ)) 0 with h | h
    · rw [max_eq_left h, max_eq_left (by linarith [(hx a).2]),
        max_eq_left (by linarith [(hx a).2])]
    · rw [max_eq_right h]
      congr 1
      ring

omit [Fintype I] [DecidableEq I] in
/-- Exact lower envelope, including the empty support (the constant monomial one). -/
theorem monomial_minimum [Finite I] (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    IsLeast (envelopeValues (monomial s) x)
      (max 0 ((∑ i ∈ s, x i) - (s.card - 1 : ℝ))) := by
  classical
  let := Fintype.ofFinite I
  apply minimum_from_laws _ (monomial_coordinate_affine s)
  · intro μ hmean
    exact max_le (monomial_expect_nonneg s μ) (monomial_expect_lower s μ x hmean)
  · exact monomial_lower_attaining_law s x hx

/-- The full graph-hull width of a nonempty monomial is its smallest mean minus
its Fréchet lower envelope. -/
theorem monomial_hullGap_of_min_coordinate (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) (i : I) (hi : i ∈ s) (hmin : ∀ j ∈ s, x i ≤ x j) :
    hullGap (monomial s) x =
      x i - max 0 ((∑ j ∈ s, x j) - (s.card - 1 : ℝ)) := by
  rw [hullGap, (monomial_maximum_of_min_coordinate s x hx i hi hmin).csSup_eq,
    (monomial_minimum s x hx).csInf_eq]

/-- Coordinate-free form of the exact nonempty monomial gap formula. -/
theorem monomial_hullGap (s : Finset I) (hs : s.Nonempty) (x : I → ℝ)
    (hx : x ∈ cube I) :
    hullGap (monomial s) x =
      s.inf' hs x - max 0 ((∑ j ∈ s, x j) - (s.card - 1 : ℝ)) := by
  obtain ⟨i, hi, heq⟩ := Finset.exists_mem_eq_inf' hs x
  rw [heq]
  apply monomial_hullGap_of_min_coordinate s x hx i hi
  intro j hj
  rw [← heq]
  exact Finset.inf'_le x hj

/-- The empty support has the constant value one and therefore has zero width. -/
theorem empty_monomial_hullGap (x : I → ℝ) (hx : x ∈ cube I) :
    hullGap (monomial (∅ : Finset I)) x = 0 := by
  have hmin : IsLeast (envelopeValues (monomial (∅ : Finset I)) x) 1 := by
    simpa using monomial_minimum ∅ x hx
  have hmax : IsGreatest (envelopeValues (monomial (∅ : Finset I)) x) 1 := by
    refine ⟨hmin.1, ?_⟩
    intro z hz
    obtain ⟨μ, _, hμ⟩ := (mem_cubeGraph_hull_iff (monomial (∅ : Finset I))
      (monomial_coordinate_affine ∅) x z).mp hz
    simpa [monomial] using hμ.symm.le
  rw [hullGap, hmax.csSup_eq, hmin.csInf_eq, sub_self]

end
end MultilinearGap
