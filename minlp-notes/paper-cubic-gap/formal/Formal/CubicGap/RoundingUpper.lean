import Formal.CubicGap.RoundingLaws
import Formal.MultilinearGap.MonomialEnvelope
import Formal.MultilinearGap.BoxSuprema

/-! The common cubic rounding law bounds every polynomial of degree at most
three, including constants and linear terms, on every nonnegative box. -/

namespace CubicGap
open MultilinearGap
noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] in
theorem support_pair_sorted (s : Finset I) (hs : s.card = 2) (x : I → ℝ) :
    ∃ i j, i ≠ j ∧ s = {i,j} ∧ x i ≤ x j := by
  obtain ⟨i,j,hij,rfl⟩ := Finset.card_eq_two.mp hs
  rcases le_total (x i) (x j) with h | h
  · exact ⟨i,j,hij,rfl,h⟩
  · exact ⟨j,i,hij.symm,Finset.pair_comm _ _,h⟩

omit [Fintype I] in
theorem support_triple_sorted (s : Finset I) (hs : s.card = 3) (x : I → ℝ) :
    ∃ i j k, i ≠ j ∧ i ≠ k ∧ j ≠ k ∧ s = {i,j,k} ∧ x i ≤ x j ∧ x j ≤ x k := by
  obtain ⟨i,j,k,hij,hik,hjk,rfl⟩ := Finset.card_eq_three.mp hs
  rcases le_total (x i) (x j) with h₁ | h₁
  · rcases le_total (x j) (x k) with h₂ | h₂
    · exact ⟨i,j,k,hij,hik,hjk,rfl,h₁,h₂⟩
    · rcases le_total (x i) (x k) with h₃ | h₃
      · exact ⟨i,k,j,hik,hij,hjk.symm,by ext; simp; tauto,h₃,h₂⟩
      · exact ⟨k,i,j,hik.symm,hjk.symm,hij,by ext; simp; tauto,h₃,h₁⟩
  · rcases le_total (x i) (x k) with h₂ | h₂
    · exact ⟨j,i,k,hij.symm,hjk,hik,by ext; simp; tauto,h₁,h₂⟩
    · rcases le_total (x j) (x k) with h₃ | h₃
      · exact ⟨j,k,i,hjk,hij.symm,hik.symm,by ext; simp; tauto,h₃,h₂⟩
      · exact ⟨k,j,i,hjk.symm,hik.symm,hij.symm,by ext; simp; tauto,h₃,h₁⟩

theorem pair_hullGap (x : I → ℝ) (hx : x ∈ cube I) (i j : I)
    (hij : i ≠ j) (horder : x i ≤ x j) :
    hullGap (monomial {i,j}) x = min (x i) (1 - x j) := by
  rw [monomial_hullGap_of_min_coordinate _ x hx i (by simp) (by
    intro k hk
    simp only [Finset.mem_insert, Finset.mem_singleton] at hk
    rcases hk with rfl | rfl
    · exact le_refl _
    · exact horder)]
  simp only [Finset.sum_insert (show i ∉ ({j} : Finset I) by simp [hij]),
    Finset.sum_singleton, Finset.card_pair hij]
  norm_num only [Nat.cast_ofNat]
  simp only [max_def, min_def]
  split_ifs <;> linarith

theorem triple_hullGap (x : I → ℝ) (hx : x ∈ cube I) (i j k : I)
    (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k)
    (horder : x i ≤ x j) (horder' : x j ≤ x k) :
    hullGap (monomial {i,j,k}) x = min (x i) (2 - x j - x k) := by
  rw [monomial_hullGap_of_min_coordinate _ x hx i (by simp) (by
    intro a ha
    simp only [Finset.mem_insert, Finset.mem_singleton] at ha
    rcases ha with rfl | rfl | rfl
    · exact le_refl _
    · exact horder
    · exact horder.trans horder')]
  have hc : ({i,j,k} : Finset I).card = 3 :=
    Finset.card_eq_three.mpr ⟨i,j,k,hij,hik,hjk,rfl⟩
  simp only [Finset.sum_insert (show i ∉ ({j,k} : Finset I) by simp [hij,hik]),
    Finset.sum_insert (show j ∉ ({k} : Finset I) by simp [hjk]),
    Finset.sum_singleton, hc]
  norm_num only [Nat.cast_ofNat]
  simp only [max_def, min_def]
  split_ifs <;> linarith

/-- A common law's sorted pair and triple estimates cover every support of
cardinality at most three. -/
theorem small_support_deficiency (x : I → ℝ) (hx : x ∈ cube I)
    (μ : Law (Vertex I)) (hm : HasMeans μ x)
    (hp : ∀ i j, i ≠ j → x i ≤ x j →
      12 * min (x i) (1 - x j) ≤
        31 * (x i - μ.expect (fun v => monomial {i,j} (vertexPoint v))))
    (ht : ∀ i j k, i ≠ j → i ≠ k → j ≠ k → x i ≤ x j → x j ≤ x k →
      12 * min (x i) (2 - x j - x k) ≤
        31 * (x i - μ.expect (fun v => monomial {i,j,k} (vertexPoint v))))
    (s : Finset I) (hs : s.card ≤ 3) :
    (12 / 31 : ℝ) * hullGap (monomial s) x ≤
      monomialUpper s x - μ.expect (fun v => monomial s (vertexPoint v)) := by
  have hcard : s.card = 0 ∨ s.card = 1 ∨ s.card = 2 ∨ s.card = 3 := by omega
  rcases hcard with hc | hc | hc | hc
  · have he := Finset.card_eq_zero.mp hc
    subst s
    simp [monomial_gap_empty x hx, monomial]
  · obtain ⟨i,rfl⟩ := Finset.card_eq_one.mp hc
    have hgap : hullGap (monomial {i}) x = 0 := by
      rw [monomial_hullGap_of_min_coordinate _ x hx i (by simp) (by simp)]
      simp [max_eq_right (hx i).1]
    have hu : monomialUpper {i} x = x i :=
      monomialUpper_eq_anchor _ x i (by simp) (by simp)
    have he : μ.expect (fun v => monomial {i} (vertexPoint v)) = x i := by
      simpa [monomial] using hm i
    simp [hgap,hu,he]
  · obtain ⟨i,j,hij,rfl,horder⟩ := support_pair_sorted s hc x
    have hu : monomialUpper {i,j} x = x i := by
      apply monomialUpper_eq_anchor _ x i (by simp)
      intro k hk
      simp only [Finset.mem_insert, Finset.mem_singleton] at hk
      rcases hk with rfl | rfl
      · exact le_refl _
      · exact horder
    rw [pair_hullGap x hx i j hij horder, hu]
    linarith [hp i j hij horder]
  · obtain ⟨i,j,k,hij,hik,hjk,rfl,horder,horder'⟩ := support_triple_sorted s hc x
    have hu : monomialUpper {i,j,k} x = x i := by
      apply monomialUpper_eq_anchor _ x i (by simp)
      intro a ha
      simp only [Finset.mem_insert, Finset.mem_singleton] at ha
      rcases ha with rfl | rfl | rfl
      · exact le_refl _
      · exact horder
      · exact horder.trans horder'
    rw [triple_hullGap x hx i j k hij hik hjk horder horder', hu]
    linarith [ht i j k hij hik hjk horder horder']

/-- A single bilinear monomial supplies a positive-gap cubic-ratio witness. -/
theorem degreeRatios_three_nonempty : (degreeRatios 3).Nonempty := by
  let S : Finset (Finset (Fin 2)) := {{0,1}}
  let x : Fin 2 → ℝ := fun _ => 1 / 2
  have hx : x ∈ cube (Fin 2) := by intro i; norm_num [x]
  have hg : hullGap (monomial ({0,1} : Finset (Fin 2))) x = 1 / 2 := by
    rw [pair_hullGap x hx 0 1 (by decide) (by simp [x])]
    norm_num [x]
  have hf : supportPolynomial S (fun _ => (1 : ℝ)) = monomial {0,1} := by
    funext y
    simp [S, supportPolynomial]
  refine ⟨1, Fin 2, inferInstance, inferInstance, S, fun _ => 1, x,
    by simp, ?_, hx, ?_, ?_⟩
  · intro s hs
    have he : s = {0,1} := by simpa [S] using hs
    subst s
    simp
  · rw [hf,hg]
    norm_num
  · rw [hf,hg]
    simp [S, weightedTermwiseGap, hg]

/-- The fixed ambient law captures at least `12/31` of every monomial gap
of degree at most three. No choice depends on the monomial support. -/
theorem cubicRoundingLaw_support_deficiency (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) (hs : s.card ≤ 3) :
    (12 / 31 : ℝ) * hullGap (monomial s) x ≤
      monomialUpper s x -
        (cubicRoundingLaw x hx).expect (fun v => monomial s (vertexPoint v)) := by
  exact small_support_deficiency x hx (cubicRoundingLaw x hx)
    (cubicRoundingLaw_hasMeans x hx)
    (fun i j hij hijx => cubicRoundingLaw_pair_deficiency_lower x hx i j hij hijx)
    (fun i j k hij hik hjk hijx hjkx =>
      cubicRoundingLaw_triple_deficiency_lower x hx i j k hij hik hjk hijx hjkx) s hs

/-- Universal cubic bound for the actual continuous graph-hull gaps. -/
theorem cubic_cube_gap_bound (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (hd : ∀ s ∈ supports, s.card ≤ 3) (x : I → ℝ) (hx : x ∈ cube I) :
    weightedTermwiseGap supports a x ≤
      (31 / 12 : ℝ) * hullGap (supportPolynomial supports a) x := by
  have h := coupling_gap_bound_general supports a ha x hx (12 / 31) (by norm_num)
    (cubicRoundingLaw x hx) (cubicRoundingLaw_hasMeans x hx)
    (fun s hs => cubicRoundingLaw_support_deficiency s x hx (hd s hs))
  norm_num only [one_div_div] at h
  exact h

/-- Dimension-independent degree-three cube guarantee. -/
theorem cubic_degree_bound : CubeDegreeBound 3 (31 / 12) := by
  intro I _ _ supports a x ha hd hx
  exact cubic_cube_gap_bound supports a ha hd x hx

omit [Fintype I] [DecidableEq I] in
/-- The cubic bound on every original finite nonnegative box, including boxes
with fixed coordinates and polynomials with zero coefficients. -/
theorem cubic_box_gap_bound [Finite I] (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (hd : ∀ s ∈ supports, s.card ≤ 3) (l u : I → ℝ)
    (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    boxTermwiseGap supports a l u x ≤
      (31 / 12 : ℝ) * boxHullGap l u (supportPolynomial supports a) x := by
  classical
  let := Fintype.ofFinite I
  exact degree_gap_bound_on_box 3 (31 / 12)
    (fun S b hb hd p hp => cubic_cube_gap_bound S b hb hd p hp)
    supports a ha hd l u hl hlu x hx

/-- Upper bound on the supremum over all finite dimensions on the cube. -/
theorem cubic_degreeSupremum_le : degreeSupremum 3 ≤ (31 / 12 : ℝ) := by
  exact csSup_le degreeRatios_three_nonempty (fun _ hr => degreeRatios_le cubic_degree_bound hr)

/-- Upper bound on the supremum over all finite nonnegative boxes. -/
theorem cubic_boxDegreeSupremum_le : boxDegreeSupremum 3 ≤ (31 / 12 : ℝ) := by
  apply csSup_le (degreeRatios_three_nonempty.mono (degreeRatios_subset_boxDegreeRatios 3))
  exact fun _ hr => boxDegreeRatios_le cubic_degree_bound hr

end
end CubicGap
