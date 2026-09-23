import Formal.MultilinearGap.StructuralCardinality

/-!
# Common upper law for convex cardinality objectives

The common-threshold law maximizes every discretely convex function of a
support's success count. Convexity is required only on the attainable counts;
neither positivity nor monotonicity of the objective is required.
-/

namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] in
/-- Removing a coordinate separates its binary contribution to the count. -/
theorem countOn_erase_add {s : Finset I} {a : I} (ha : a ∈ s) (v : Vertex I) :
    countOn s v = countOn (s.erase a) v + if v a = true then 1 else 0 := by
  by_cases hv : v a = true
  · have hmem : a ∈ s.filter (fun i => v i = true) := by simp [ha, hv]
    have heq : (s.erase a).filter (fun i => v i = true) =
        (s.filter (fun i => v i = true)).erase a := by ext; simp; tauto
    simpa [countOn, hv, heq] using (Finset.card_erase_add_one hmem).symm
  · have heq : (s.erase a).filter (fun i => v i = true) =
        s.filter (fun i => v i = true) := by
      ext i
      simp only [Finset.mem_filter, Finset.mem_erase]
      constructor
      · tauto
      · rintro ⟨hi, hvi⟩
        exact ⟨⟨by intro h; subst i; exact hv hvi, hi⟩, hvi⟩
    simp [countOn, hv, heq]

/-- Restricted convexity orders the first differences used by the objective. -/
theorem cardinality_increment_le (φ : ℕ → ℝ) {n : ℕ}
    (hφ : ConvexCountTable φ n) {k l : ℕ} (hkl : k ≤ l) (hl : l + 1 ≤ n) :
    φ (k + 1) - φ k ≤ φ (l + 1) - φ l := by
  induction hkl with
  | refl => exact le_rfl
  | @step l hkl ih => exact (ih (by omega)).trans (hφ l (by omega))

/-- A positive-weight threshold vertex containing a minimum-mean coordinate
contains the whole support. -/
theorem thresholdLaw_support_of_min {s : Finset I} {a : I} (ha : a ∈ s)
    (x : I → ℝ) (hx : x ∈ cube I) (hmin : ∀ i ∈ s, x a ≤ x i)
    (v : Vertex I) (hw : (thresholdLaw x).weight v ≠ 0) (hva : v a = true) :
    ∀ i ∈ s, v i = true := by
  let μ := thresholdLaw x
  have hnonneg (w : Vertex I) :
      0 ≤ μ.weight w * (vertexPoint w a - monomial s (vertexPoint w)) := by
    apply mul_nonneg (μ.nonneg w)
    exact sub_nonneg.mpr (monomial_le_coordinate s (by
      intro i _; simp only [vertexPoint]; split <;> norm_num) ha)
  have he : μ.expect (fun w => vertexPoint w a - monomial s (vertexPoint w)) = 0 := by
    rw [Law.expect_sub, thresholdLaw_hasMeans x hx a, thresholdLaw_monomial s x hx a ha hmin]
    exact sub_self _
  have hz : μ.weight v * (vertexPoint v a - monomial s (vertexPoint v)) = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg (fun w _ => hnonneg w)).mp he v (Finset.mem_univ v)
  have hp : monomial s (vertexPoint v) = 1 := by
    have := (mul_eq_zero.mp hz).resolve_left hw
    simpa [vertexPoint, hva] using (sub_eq_zero.mp this).symm
  intro i hi
  by_contra hvi
  have hzero : monomial s (vertexPoint v) = 0 :=
    Finset.prod_eq_zero hi (by simp [vertexPoint, hvi])
  linarith

/-- Peeling a minimum-mean coordinate gives an exact recurrence for the
common-threshold expectation, for any cardinality objective. -/
theorem thresholdLaw_cardinality_peel (φ : ℕ → ℝ) {s : Finset I} {a : I}
    (ha : a ∈ s) (x : I → ℝ) (hx : x ∈ cube I)
    (hmin : ∀ i ∈ s, x a ≤ x i) :
    (thresholdLaw x).expect (fun v => φ (countOn s v)) =
      (thresholdLaw x).expect (fun v => φ (countOn (s.erase a) v)) +
        x a * (φ s.card - φ (s.erase a).card) := by
  have he : (thresholdLaw x).expect (fun v => φ (countOn s v)) =
      (thresholdLaw x).expect (fun v => φ (countOn (s.erase a) v) +
        vertexPoint v a * (φ s.card - φ (s.erase a).card)) := by
    apply Finset.sum_congr rfl
    intro v _
    by_cases hw : (thresholdLaw x).weight v = 0
    · simp [hw]
    congr 1
    dsimp only
    by_cases hv : v a = true
    · have hall := thresholdLaw_support_of_min ha x hx hmin v hw hv
      have hs : countOn s v = s.card := by simp [countOn, Finset.filter_eq_self.mpr hall]
      have ht : countOn (s.erase a) v = (s.erase a).card := by
        simp [countOn, Finset.filter_eq_self.mpr (fun i hi => hall i (Finset.mem_of_mem_erase hi))]
      simp [hs, ht, vertexPoint, hv]
    · rw [countOn_erase_add ha]
      simp [vertexPoint, hv]
  rw [he, Law.expect_add, Law.expect_mul_const, thresholdLaw_hasMeans x hx a]

/-- The same common-threshold law maximizes every convex cardinality objective
on every support, including signed or nonmonotone objectives. -/
theorem convex_cardinality_common_upper (s : Finset I) (φ : ℕ → ℝ)
    (hφ : ConvexCountTable φ s.card)
    (x : I → ℝ) (hx : x ∈ cube I) (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    μ.expect (fun v => φ (countOn s v)) ≤
      (thresholdLaw x).expect (fun v => φ (countOn s v)) := by
  revert hφ
  refine Finset.strongInductionOn s ?_
  intro s ih hφ
  by_cases hs : s.Nonempty
  · obtain ⟨a, ha, hmin⟩ := monomial_min_anchor s hs x
    have hc := Finset.card_erase_add_one ha
    have hφ' : ConvexCountTable φ (s.erase a).card := fun k hk => hφ k (by omega)
    have hb (v : Vertex I) : φ (countOn s v) ≤
        φ (countOn (s.erase a) v) + vertexPoint v a * (φ s.card - φ (s.erase a).card) := by
      rw [countOn_erase_add ha]
      by_cases hv : v a = true
      · simp only [hv, if_true, vertexPoint, one_mul]
        have hd := cardinality_increment_le φ hφ (countOn_le_card (s.erase a) v)
          (show (s.erase a).card + 1 ≤ s.card by omega)
        rw [hc] at hd
        linarith
      · simp [vertexPoint, hv]
    calc μ.expect (fun v => φ (countOn s v))
        ≤ μ.expect (fun v => φ (countOn (s.erase a) v) +
            vertexPoint v a * (φ s.card - φ (s.erase a).card)) := μ.expect_mono hb
      _ = μ.expect (fun v => φ (countOn (s.erase a) v)) +
            x a * (φ s.card - φ (s.erase a).card) := by
          rw [Law.expect_add, Law.expect_mul_const, hm a]
      _ ≤ (thresholdLaw x).expect (fun v => φ (countOn (s.erase a) v)) +
            x a * (φ s.card - φ (s.erase a).card) := by
          have h := ih (s.erase a) (Finset.erase_ssubset ha) hφ'
          linarith
      _ = (thresholdLaw x).expect (fun v => φ (countOn s v)) :=
          (thresholdLaw_cardinality_peel φ ha x hx hmin).symm
  · have : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp hs
    subst s
    simp

/-- The common-threshold expectation is the exact upper endpoint of the
continuous graph hull of any separately affine interpolant of the table. -/
theorem cardinality_maximum (φ : ℕ → ℝ) (s : Finset I)
    (hφ : ConvexCountTable φ s.card) (f : (I → ℝ) → ℝ)
    (hf : SeparatelyAffine f)
    (hv : ∀ v : Vertex I, f (vertexPoint v) = φ (countOn s v))
    (x : I → ℝ) (hx : x ∈ cube I) :
    IsGreatest (envelopeValues f x)
      ((thresholdLaw x).expect (fun v => φ (countOn s v))) := by
  apply maximum_from_laws f hf
  · intro μ hm
    simp only [hv]
    exact convex_cardinality_common_upper s φ hφ x hx μ hm
  · exact ⟨thresholdLaw x, thresholdLaw_hasMeans x hx, by simp only [hv]⟩

/-- Nonnegative sums of convex cardinality factors attain their upper
endpoints simultaneously, even with overlapping supports. -/
theorem convex_cardinality_sum_common_upper {A : Type*} (terms : Finset A)
    (support : A → Finset I) (φ : A → ℕ → ℝ) (coefficient : A → ℝ)
    (hcoefficient : ∀ a ∈ terms, 0 ≤ coefficient a)
    (hφ : ∀ a ∈ terms, ConvexCountTable (φ a) (support a).card)
    (x : I → ℝ) (hx : x ∈ cube I) (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    μ.expect (fun v => ∑ a ∈ terms, coefficient a * φ a (countOn (support a) v)) ≤
      (thresholdLaw x).expect
        (fun v => ∑ a ∈ terms, coefficient a * φ a (countOn (support a) v)) := by
  have he (ν : Law (Vertex I)) :
      ν.expect (fun v => ∑ a ∈ terms, coefficient a * φ a (countOn (support a) v)) =
        ∑ a ∈ terms, coefficient a * ν.expect (fun v => φ a (countOn (support a) v)) := by
    unfold Law.expect
    simp only [Finset.mul_sum]
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl fun a _ => Finset.sum_congr rfl fun v _ => by ring
  rw [he μ, he (thresholdLaw x)]
  exact Finset.sum_le_sum fun a ha => mul_le_mul_of_nonneg_left
    (convex_cardinality_common_upper (support a) (φ a) (hφ a ha) x hx μ hm)
    (hcoefficient a ha)

end
end MultilinearGap
