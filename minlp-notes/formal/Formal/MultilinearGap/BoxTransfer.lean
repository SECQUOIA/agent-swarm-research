import Formal.MultilinearGap.GeneralGaps

/-! Affine box rescaling and the positive squarefree expansion it induces. -/

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- A finite coordinate box, allowing zero width coordinates. -/
def coordinateBox (l u : I → ℝ) : Set (I → ℝ) :=
  {x | ∀ i, l i ≤ x i ∧ x i ≤ u i}

/-- The usual affine parameterization of a coordinate box. -/
def boxPoint (l u p : I → ℝ) : I → ℝ := fun i => l i + (u i - l i) * p i

/-- The continuous graph on the original box. -/
def boxGraph (l u : I → ℝ) (f : (I → ℝ) → ℝ) : Set ((I → ℝ) × ℝ) :=
  {q | q.1 ∈ coordinateBox l u ∧ q.2 = f q.1}

def boxEnvelopeValues (l u : I → ℝ) (f : (I → ℝ) → ℝ) (x : I → ℝ) : Set ℝ :=
  {z | (x, z) ∈ convexHull ℝ (boxGraph l u f)}

def boxHullGap (l u : I → ℝ) (f : (I → ℝ) → ℝ) (x : I → ℝ) : ℝ :=
  sSup (boxEnvelopeValues l u f x) - sInf (boxEnvelopeValues l u f x)

private def boxGraphMap (l u : I → ℝ) : ((I → ℝ) × ℝ) →ᵃ[ℝ] ((I → ℝ) × ℝ) where
  toFun q := (boxPoint l u q.1, q.2)
  linear := {
    toFun q := (fun i => (u i - l i) * q.1 i, q.2)
    map_add' := by intros; ext <;> simp [mul_add]
    map_smul' := by intros; ext <;> simp [mul_left_comm] }
  map_vadd' := by intros; ext <;> simp [boxPoint]; ring

omit [Fintype I] [DecidableEq I] in
theorem boxPoint_mem (l u p : I → ℝ) (hlu : ∀ i, l i ≤ u i) (hp : p ∈ cube I) :
    boxPoint l u p ∈ coordinateBox l u := by
  intro i
  have := hp i
  have := hlu i
  dsimp [boxPoint]
  constructor <;> nlinarith

private def fixedGraphMap (l u p : I → ℝ) : ((I → ℝ) × ℝ) →ᵃ[ℝ] ((I → ℝ) × ℝ) where
  toFun q := (fun i => if l i = u i then p i else q.1 i, q.2)
  linear := {
    toFun q := (fun i => if l i = u i then 0 else q.1 i, q.2)
    map_add' := by
      intro q r
      apply Prod.ext
      · funext i; change (if l i = u i then 0 else q.1 i + r.1 i) = _
        split_ifs <;> simp_all
      · rfl
    map_smul' := by
      intro c q
      apply Prod.ext
      · funext i; change (if l i = u i then 0 else c * q.1 i) = _
        split_ifs <;> simp_all
      · rfl }
  map_vadd' := by
    intro q r
    apply Prod.ext
    · funext i
      change (if l i = u i then p i else r.1 i + q.1 i) =
        (if l i = u i then 0 else r.1 i) + (if l i = u i then p i else q.1 i)
      split_ifs <;> simp_all
    · rfl

omit [Fintype I] [DecidableEq I] in
private theorem boxGraphMap_image_of_le (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) :
    boxGraphMap l u '' cubeGraph (fun p => f (boxPoint l u p)) = boxGraph l u f := by
  ext q
  constructor
  · rintro ⟨p, hp, rfl⟩
    exact ⟨boxPoint_mem l u p.1 hlu hp.1, hp.2⟩
  · intro hq
    let p : I → ℝ := fun i => (q.1 i - l i) / (u i - l i)
    have hp : p ∈ cube I := by
      intro i
      by_cases he : l i = u i
      · simp [p, he]
      · have hd : 0 < u i - l i := sub_pos.mpr (lt_of_le_of_ne (hlu i) he)
        exact ⟨div_nonneg (sub_nonneg.mpr (hq.1 i).1) hd.le,
          (div_le_one hd).mpr (sub_le_sub_right (hq.1 i).2 _)⟩
    have he : boxPoint l u p = q.1 := by
      funext i
      dsimp [boxPoint, p]
      by_cases he : l i = u i
      · have hx := hq.1 i
        simp only [he, sub_self, zero_mul, add_zero]
        linarith
      · rw [mul_div_cancel₀ _ (sub_ne_zero.mpr (Ne.symm he))]
        ring
    refine ⟨(p, q.2), ⟨hp, ?_⟩, ?_⟩
    · simpa [he] using hq.2
    · change (boxPoint l u p, q.2) = q
      simp [he]

omit [Fintype I] [DecidableEq I] in
/-- Zero width coordinates cause no loss: reset their arbitrary cube means to
the requested point while keeping every graph value unchanged. -/
theorem boxEnvelopeValues_eq_of_mem (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) (p : I → ℝ) (hp : p ∈ cube I) :
    boxEnvelopeValues l u f (boxPoint l u p) =
      envelopeValues (fun q => f (boxPoint l u q)) p := by
  have himage := (boxGraphMap l u).image_convexHull
    (cubeGraph (fun q => f (boxPoint l u q)))
  rw [boxGraphMap_image_of_le l u hlu f] at himage
  ext z
  change (boxPoint l u p, z) ∈ convexHull ℝ (boxGraph l u f) ↔ _
  rw [← himage]
  constructor
  · rintro ⟨⟨q, w⟩, hq, he⟩
    have hreset : fixedGraphMap l u p '' cubeGraph (fun q => f (boxPoint l u q)) ⊆
        cubeGraph (fun q => f (boxPoint l u q)) := by
      rintro _ ⟨r, hr, rfl⟩
      constructor
      · intro i
        change 0 ≤ (if l i = u i then p i else r.1 i) ∧
          (if l i = u i then p i else r.1 i) ≤ 1
        split_ifs
        · exact hp i
        · exact hr.1 i
      · change r.2 = f (boxPoint l u (fun i => if l i = u i then p i else r.1 i))
        have heq : boxPoint l u (fun i => if l i = u i then p i else r.1 i) =
            boxPoint l u r.1 := by
          funext i
          dsimp [boxPoint]
          split_ifs with hi
          · simp [hi]
          · rfl
        rw [heq]
        exact hr.2
    have hmem := convexHull_mono (𝕜 := ℝ) hreset
    rw [← (fixedGraphMap l u p).image_convexHull] at hmem
    have hq' := hmem (Set.mem_image_of_mem (fixedGraphMap l u p) hq)
    have hfix : fixedGraphMap l u p (q, w) = (p, z) := by
      apply Prod.ext
      · funext i
        change (if l i = u i then p i else q i) = p i
        split_ifs with hi
        · rfl
        · have hei := congrFun (congrArg Prod.fst he) i
          exact mul_left_cancel₀ (sub_ne_zero.mpr (Ne.symm hi)) (add_left_cancel hei)
      · change w = z
        exact congrArg Prod.snd he
    rw [hfix] at hq'
    exact hq'
  · intro hz
    exact ⟨(p, z), hz, rfl⟩

theorem boxHullGap_eq_of_mem (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) (p : I → ℝ) (hp : p ∈ cube I) :
    boxHullGap l u f (boxPoint l u p) = hullGap (fun q => f (boxPoint l u q)) p := by
  simp only [boxHullGap, hullGap, boxEnvelopeValues_eq_of_mem l u hlu f p hp]

/-- The coefficient of a squarefree subterm after affine rescaling. -/
def boxExpansionCoefficient (l u : I → ℝ) (s t : Finset I) : ℝ :=
  (∏ i ∈ t, (u i - l i)) * ∏ i ∈ s \ t, l i

omit [Fintype I] in
/-- Rescaling a monomial produces exactly its powerset expansion. -/
theorem monomial_box_expansion (l u p : I → ℝ) (s : Finset I) :
    monomial s (boxPoint l u p) =
      supportPolynomial s.powerset (boxExpansionCoefficient l u s) p := by
  unfold monomial boxPoint supportPolynomial boxExpansionCoefficient
  simp_rw [add_comm (l _) ((_ - _) * _)]
  rw [Finset.prod_add]
  apply Finset.sum_congr rfl
  intro t _
  rw [Finset.prod_mul_distrib]
  unfold monomial
  ring

omit [Fintype I] in
theorem boxExpansionCoefficient_nonneg (l u : I → ℝ)
    (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i) (s t : Finset I) :
    0 ≤ boxExpansionCoefficient l u s t := by
  exact mul_nonneg (Finset.prod_nonneg fun i _ => sub_nonneg.mpr (hlu i))
    (Finset.prod_nonneg fun i _ => hl i)

omit [Fintype I] [DecidableEq I] in
/-- Affine expansion cannot increase the degree of any original term. -/
theorem boxExpansion_degree (s t : Finset I) (ht : t ∈ s.powerset) : t.card ≤ s.card :=
  Finset.card_le_card (Finset.mem_powerset.mp ht)


/-- All squarefree terms that can occur after rescaling. -/
def boxExpansionSupports (supports : Finset (Finset I)) : Finset (Finset I) :=
  supports.biUnion Finset.powerset

/-- Coefficients of equal subterms are collected after expansion. -/
def boxPolynomialCoefficient (supports : Finset (Finset I)) (a : Finset I → ℝ)
    (l u : I → ℝ) (t : Finset I) : ℝ :=
  ∑ s ∈ supports, if t ⊆ s then a s * boxExpansionCoefficient l u s t else 0

omit [Fintype I] in
theorem boxPolynomialCoefficient_nonneg (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (t : Finset I) : 0 ≤ boxPolynomialCoefficient supports a l u t := by
  apply Finset.sum_nonneg
  intro s hs
  split_ifs
  · exact mul_nonneg (ha s hs) (boxExpansionCoefficient_nonneg l u hl hlu s t)
  · exact le_rfl

omit [Fintype I] in
theorem boxPolynomialExpansion_sum (supports : Finset (Finset I))
    (a : Finset I → ℝ) (l u : I → ℝ) (v : Finset I → ℝ) :
    (∑ t ∈ boxExpansionSupports supports,
      boxPolynomialCoefficient supports a l u t * v t) =
      ∑ s ∈ supports, a s * ∑ t ∈ s.powerset, boxExpansionCoefficient l u s t * v t := by
  simp only [boxPolynomialCoefficient, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro s hs
  rw [Finset.mul_sum]
  have hsub : s.powerset ⊆ boxExpansionSupports supports := by
    intro t ht
    exact Finset.mem_biUnion.mpr ⟨s, hs, ht⟩
  calc
    _ = ∑ t ∈ s.powerset,
        (if t ⊆ s then a s * boxExpansionCoefficient l u s t else 0) * v t := by
      symm
      apply Finset.sum_subset hsub
      intro t _ ht
      simp [show ¬t ⊆ s from fun h => ht (Finset.mem_powerset.mpr h)]
    _ = _ := by
      apply Finset.sum_congr rfl
      intro t ht
      rw [if_pos (Finset.mem_powerset.mp ht)]
      ring

omit [Fintype I] in
/-- The expanded polynomial agrees everywhere with the rescaled original. -/
theorem supportPolynomial_box_expansion (supports : Finset (Finset I))
    (a : Finset I → ℝ) (l u p : I → ℝ) :
    supportPolynomial supports a (boxPoint l u p) =
      supportPolynomial (boxExpansionSupports supports)
        (boxPolynomialCoefficient supports a l u) p := by
  simp only [supportPolynomial]
  rw [boxPolynomialExpansion_sum]
  apply Finset.sum_congr rfl
  intro s _
  rw [monomial_box_expansion]
  rfl

omit [Fintype I] in
theorem boxPolynomialExpansion_degree (supports : Finset (Finset I)) (d : ℕ)
    (hd : ∀ s ∈ supports, s.card ≤ d) (t : Finset I)
    (ht : t ∈ boxExpansionSupports supports) : t.card ≤ d := by
  obtain ⟨s, hs, hts⟩ := Finset.mem_biUnion.mp ht
  exact (boxExpansion_degree s t hts).trans (hd s hs)


/-- The original term-by-term relaxation on a box. -/
def boxTermwiseGap (supports : Finset (Finset I)) (a : Finset I → ℝ)
    (l u x : I → ℝ) : ℝ :=
  ∑ s ∈ supports, a s * boxHullGap l u (monomial s) x

/-- Expanding each rescaled monomial can only enlarge its termwise gap. -/
theorem boxTermwiseGap_le_expansion (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (p : I → ℝ) (hp : p ∈ cube I) :
    boxTermwiseGap supports a l u (boxPoint l u p) ≤
      weightedTermwiseGap (boxExpansionSupports supports)
        (boxPolynomialCoefficient supports a l u) p := by
  unfold boxTermwiseGap weightedTermwiseGap
  rw [boxPolynomialExpansion_sum]
  apply Finset.sum_le_sum
  intro s hs
  apply mul_le_mul_of_nonneg_left _ (ha s hs)
  rw [boxHullGap_eq_of_mem l u hlu _ p hp]
  have he : (fun q => monomial s (boxPoint l u q)) =
      supportPolynomial s.powerset (boxExpansionCoefficient l u s) := by
    funext q
    exact monomial_box_expansion l u q s
  rw [he]
  exact hullGap_le_weightedTermwiseGap s.powerset (boxExpansionCoefficient l u s)
    (fun t _ => boxExpansionCoefficient_nonneg l u hl hlu s t) p hp

/-- Any degree-uniform cube bound transfers to the original termwise relaxation
on all finite nonnegative boxes, including fixed coordinates. -/
theorem degree_gap_bound_box_transfer (d : ℕ) (C : ℝ)
    (hbound : ∀ (S : Finset (Finset I)) (b : Finset I → ℝ),
      (∀ s ∈ S, 0 ≤ b s) → (∀ s ∈ S, s.card ≤ d) →
      ∀ p ∈ cube I, weightedTermwiseGap S b p ≤ C * hullGap (supportPolynomial S b) p)
    (supports : Finset (Finset I)) (a : Finset I → ℝ)
    (ha : ∀ s ∈ supports, 0 ≤ a s) (hd : ∀ s ∈ supports, s.card ≤ d)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (p : I → ℝ) (hp : p ∈ cube I) :
    boxTermwiseGap supports a l u (boxPoint l u p) ≤
      C * boxHullGap l u (supportPolynomial supports a) (boxPoint l u p) := by
  have he : (fun q => supportPolynomial supports a (boxPoint l u q)) =
      supportPolynomial (boxExpansionSupports supports)
        (boxPolynomialCoefficient supports a l u) := by
    funext q
    exact supportPolynomial_box_expansion supports a l u q
  rw [boxHullGap_eq_of_mem l u hlu _ p hp, he]
  exact (boxTermwiseGap_le_expansion supports a ha l u hl hlu p hp).trans
    (hbound _ _ (fun t _ => boxPolynomialCoefficient_nonneg supports a ha l u hl
      hlu t) (boxPolynomialExpansion_degree supports d hd) p hp)


omit [Fintype I] [DecidableEq I] in
/-- Every point of a finite box has a cube parameter, also for fixed coordinates. -/
theorem exists_boxPoint (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    ∃ p ∈ cube I, boxPoint l u p = x := by
  have hxg : (x, (0 : ℝ)) ∈ boxGraph l u (fun _ => 0) := ⟨hx, rfl⟩
  rw [← boxGraphMap_image_of_le l u hlu] at hxg
  obtain ⟨q, hq, he⟩ := hxg
  exact ⟨q.1, hq.1, congrArg Prod.fst he⟩

/-- The box transfer stated directly at an arbitrary original box point. -/
theorem degree_gap_bound_on_box (d : ℕ) (C : ℝ)
    (hbound : ∀ (S : Finset (Finset I)) (b : Finset I → ℝ),
      (∀ s ∈ S, 0 ≤ b s) → (∀ s ∈ S, s.card ≤ d) →
      ∀ p ∈ cube I, weightedTermwiseGap S b p ≤ C * hullGap (supportPolynomial S b) p)
    (supports : Finset (Finset I)) (a : Finset I → ℝ)
    (ha : ∀ s ∈ supports, 0 ≤ a s) (hd : ∀ s ∈ supports, s.card ≤ d)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    boxTermwiseGap supports a l u x ≤ C * boxHullGap l u (supportPolynomial supports a) x := by
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  exact degree_gap_bound_box_transfer d C hbound supports a ha hd l u hl hlu p hp

end
end MultilinearGap
