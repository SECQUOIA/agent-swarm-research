import Formal.MultilinearGap.GeneralGaps

/-! Adding unused coordinates preserves actual envelope widths and polynomial
support degrees. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I J : Type*} [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J]

def padPoint (x : I → ℝ) : I ⊕ J → ℝ := Sum.elim x (fun _ => 0)

def padFunction (f : (I → ℝ) → ℝ) (z : I ⊕ J → ℝ) : ℝ := f (z ∘ Sum.inl)

omit [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J] in
theorem padPoint_mem_cube (x : I → ℝ) (hx : x ∈ cube I) :
    padPoint (J := J) x ∈ cube (I ⊕ J) := by
  intro i
  cases i with
  | inl i => exact hx i
  | inr j => simp [padPoint]

omit [Fintype I] [Fintype J] in
theorem padFunction_separatelyAffine (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) :
    SeparatelyAffine (padFunction (J := J) f) := by
  intro z i t
  cases i with
  | inl i =>
    simp only [padFunction, Function.update_comp_eq_of_injective z Sum.inl_injective]
    exact hf (z ∘ Sum.inl) i t
  | inr j =>
    have hu (a : ℝ) : Function.update z (Sum.inr j) a ∘ Sum.inl = z ∘ Sum.inl := by
      funext i
      simp
    simp only [padFunction, hu]
    ring

omit [Fintype I] [Fintype J] [DecidableEq J] in
/-- Restricting binary laws and padding them by false coordinates gives exactly
the same vertical slices of the continuous graph hull. -/
theorem padFunction_envelopeValues [Finite I] [Finite J] (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) :
    envelopeValues (padFunction (J := J) f) (padPoint x) = envelopeValues f x := by
  classical
  let := Fintype.ofFinite I
  let := Fintype.ofFinite J
  ext z
  change (padPoint x, z) ∈ convexHull ℝ (cubeGraph (padFunction f)) ↔
    (x, z) ∈ convexHull ℝ (cubeGraph f)
  rw [mem_cubeGraph_hull_iff _ (padFunction_separatelyAffine f hf),
    mem_cubeGraph_hull_iff _ hf]
  constructor
  · rintro ⟨μ, hm, hv⟩
    refine ⟨μ.map (fun v => v ∘ Sum.inl), ?_, ?_⟩
    · intro i
      simpa [Law.expect_map, Function.comp_def, vertexPoint, padPoint] using hm (Sum.inl i)
    · rw [Law.expect_map]
      exact hv
  · rintro ⟨μ, hm, hv⟩
    refine ⟨μ.map (fun v => Sum.elim v (fun _ : J => false)), ?_, ?_⟩
    · intro i
      cases i with
      | inl i =>
        rw [Law.expect_map]
        exact hm i
      | inr j => simp [Law.expect_map, Function.comp_def, vertexPoint, padPoint]
    · rw [Law.expect_map]
      exact hv

theorem padFunction_hullGap (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) (x : I → ℝ) :
    hullGap (padFunction (J := J) f) (padPoint x) = hullGap f x := by
  simp only [hullGap, padFunction_envelopeValues f hf]

def padSupport (s : Finset I) : Finset (I ⊕ J) := s.map Function.Embedding.inl

def padSupports (S : Finset (Finset I)) : Finset (Finset (I ⊕ J)) :=
  S.image padSupport

def padCoefficient (a : Finset I → ℝ) (s : Finset (I ⊕ J)) : ℝ :=
  a (s.preimage Sum.inl Sum.inl_injective.injOn)

omit [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J] in
@[simp] theorem padCoefficient_padSupport (a : Finset I → ℝ) (s : Finset I) :
    padCoefficient a (padSupport (J := J) s) = a s := by
  unfold padCoefficient padSupport
  congr 1
  ext i
  simp only [Finset.mem_preimage, Finset.mem_map, Function.Embedding.inl_apply,
    Sum.inl.injEq, exists_eq_right]

omit [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J] in
theorem padSupport_injective : Function.Injective (padSupport (I := I) (J := J)) :=
  Finset.map_injective Function.Embedding.inl

omit [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J] in
@[simp] theorem padSupport_card (s : Finset I) : (padSupport (J := J) s).card = s.card :=
  Finset.card_map _

omit [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J] in
@[simp] theorem monomial_padSupport (s : Finset I) (z : I ⊕ J → ℝ) :
    monomial (padSupport s) z = padFunction (monomial s) z := by
  simp [monomial, padSupport, padFunction]

omit [Fintype I] [Fintype J] in
theorem padSupports_polynomial (S : Finset (Finset I)) (a : Finset I → ℝ) :
    supportPolynomial (padSupports (J := J) S) (padCoefficient a) =
      padFunction (supportPolynomial S a) := by
  funext z
  simp only [supportPolynomial, padSupports,
    Finset.sum_image (fun _ _ _ _ h => padSupport_injective h)]
  simp only [padCoefficient_padSupport, monomial_padSupport, padFunction, supportPolynomial]

omit [Fintype I] [Fintype J] in
theorem padSupports_nonnegative (S : Finset (Finset I)) (a : Finset I → ℝ)
    (ha : ∀ s ∈ S, 0 ≤ a s) :
    ∀ s ∈ padSupports (J := J) S, 0 ≤ padCoefficient a s := by
  intro s hs
  obtain ⟨t, ht, rfl⟩ := Finset.mem_image.mp hs
  simpa using ha t ht

omit [Fintype I] [Fintype J] in
theorem padSupports_degree (S : Finset (Finset I)) (d : ℕ)
    (hd : ∀ s ∈ S, s.card ≤ d) :
    ∀ s ∈ padSupports (J := J) S, s.card ≤ d := by
  intro s hs
  obtain ⟨t, ht, rfl⟩ := Finset.mem_image.mp hs
  simpa using hd t ht

theorem padSupports_hullGap (S : Finset (Finset I)) (a : Finset I → ℝ) (x : I → ℝ) :
    hullGap (supportPolynomial (padSupports (J := J) S) (padCoefficient a)) (padPoint x) =
      hullGap (supportPolynomial S a) x := by
  rw [padSupports_polynomial]
  exact padFunction_hullGap _ (supportPolynomial_coordinate_affine S a) x

theorem padSupports_weightedTermwiseGap (S : Finset (Finset I))
    (a : Finset I → ℝ) (x : I → ℝ) :
    weightedTermwiseGap (padSupports (J := J) S) (padCoefficient a) (padPoint x) =
      weightedTermwiseGap S a x := by
  simp only [weightedTermwiseGap, padSupports,
    Finset.sum_image (fun _ _ _ _ h => padSupport_injective h), padCoefficient_padSupport]
  apply Finset.sum_congr rfl
  intro s _
  congr 1
  rw [show monomial (padSupport (J := J) s) = padFunction (monomial s) by
    funext z; exact monomial_padSupport s z]
  exact padFunction_hullGap _ (monomial_coordinate_affine s) x

omit [DecidableEq I] in
/-- Padding by the missing number of coordinates realizes exactly dimension `n`. -/
theorem padded_card (n : ℕ) (hn : Fintype.card I ≤ n) :
    Fintype.card (I ⊕ Fin (n - Fintype.card I)) = n := by
  simp only [Fintype.card_sum, Fintype.card_fin]
  omega

end
end MultilinearGap
