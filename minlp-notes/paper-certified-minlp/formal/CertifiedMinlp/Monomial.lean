import CertifiedMinlp.MonomialConcave

namespace CertifiedMinlp
open Finset

variable {I : Type*} [Fintype I]

lemma realMonomial_log (a : I → ℝ) {x : I → ℝ} (hx : x ∈ positiveOrthant) :
    Real.log (realMonomial a x) = ∑ i, a i * Real.log (x i) := by
  unfold realMonomial
  rw [Real.log_prod (fun i _ ↦ (Real.rpow_pos_of_pos (hx i) _).ne')]
  exact Finset.sum_congr rfl fun i _ ↦ Real.log_rpow (hx i) _

/-- A concave geometric-mean representation of the epigraph proves convexity
of the actual monomial, without assuming a Hessian or a curvature conclusion. -/
lemma realMonomial_convex_of_lift (a b : I → ℝ) (r : ℝ) (h : (I → ℝ) → ℝ)
    (hr : 0 < r) (hb : ∀ i, 0 ≤ b i) (hs : r + ∑ i, b i ≤ 1)
    (hh : ∀ x ∈ positiveOrthant, 0 < h x)
    (haff : ∀ x y : I → ℝ, ∀ u v : ℝ, 0 ≤ u → 0 ≤ v → u + v = 1 →
      h (u • x + v • y) = u * h x + v * h y)
    (hid : ∀ x ∈ positiveOrthant,
      Real.log (h x) = r * Real.log (realMonomial a x) + ∑ i, b i * Real.log (x i)) :
    ConvexOn ℝ positiveOrthant (realMonomial a) := by
  let w : Option I → ℝ := Option.elim' r b
  have hw : ∀ i, 0 ≤ w i := by intro i; cases i <;> simp [w, hr.le, hb]
  have hws : ∑ i, w i ≤ 1 := by simpa [w, Fintype.sum_option] using hs
  have hc := realMonomial_concaveOn_positiveOrthant w hw hws
  have hconv : Convex ℝ (positiveOrthant : Set (I → ℝ)) := by
    intro x hx y hy u v hu hv huv i
    change 0 < u * x i + v * y i
    rcases lt_or_eq_of_le hu with hu | hu
    · exact add_pos_of_pos_of_nonneg (mul_pos hu (hx i)) (mul_nonneg hv (hy i).le)
    · have hv1 : v = 1 := by linarith
      simp [← hu, hv1, hy i]
  refine ⟨hconv, ?_⟩
  intro x hx y hy u v hu hv huv
  let z := u • x + v • y
  let t := u * realMonomial a x + v * realMonomial a y
  have hz : z ∈ positiveOrthant := hconv hx hy hu hv huv
  have ht : 0 < t := by
    dsimp [t]
    rcases lt_or_eq_of_le hu with hu | hu
    · exact add_pos_of_pos_of_nonneg (mul_pos hu (realMonomial_pos a x hx))
        (mul_nonneg hv (realMonomial_pos a y hy).le)
    · have hv1 : v = 1 := by linarith
      simpa [← hu, hv1] using realMonomial_pos a y hy
  let X : Option I → ℝ := Option.elim' (realMonomial a x) x
  let Y : Option I → ℝ := Option.elim' (realMonomial a y) y
  let Z : Option I → ℝ := Option.elim' t z
  have hX : X ∈ positiveOrthant := by
    intro i; cases i with
    | none => exact realMonomial_pos a x hx
    | some i => exact hx i
  have hY : Y ∈ positiveOrthant := by
    intro i; cases i with
    | none => exact realMonomial_pos a y hy
    | some i => exact hy i
  have hZ : Z ∈ positiveOrthant := by
    intro i; cases i with
    | none => exact ht
    | some i => exact hz i
  have hZX : Z = u • X + v • Y := by
    funext i; cases i <;> simp [Z, X, Y, z, t]
  have log_lift : ∀ (s : ℝ) (q : I → ℝ), 0 < s → q ∈ positiveOrthant →
      Real.log (realMonomial w (Option.elim' s q)) =
        r * Real.log s + ∑ i, b i * Real.log (q i) := by
    intro s q hs hq
    rw [realMonomial_log w (by intro i; cases i with | none => exact hs | some i => exact hq i)]
    simp [w, Fintype.sum_option]
  have lift_eq : ∀ q ∈ positiveOrthant,
      realMonomial w (Option.elim' (realMonomial a q) q) = h q := by
    intro q hq
    apply Real.log_injOn_pos
      (realMonomial_pos w _ (by
        intro i
        cases i with
        | none => exact realMonomial_pos a q hq
        | some i => exact hq i))
      (hh q hq)
    exact (log_lift _ _ (realMonomial_pos a q hq) hq).trans (hid q hq).symm
  have H := hc.2 hX hY hu hv huv
  change u * realMonomial w X + v * realMonomial w Y ≤ _ at H
  rw [← hZX] at H
  change u * realMonomial w (Option.elim' (realMonomial a x) x) +
    v * realMonomial w (Option.elim' (realMonomial a y) y) ≤ realMonomial w Z at H
  rw [lift_eq x hx, lift_eq y hy, ← haff x y u v hu hv huv] at H
  have HL := Real.log_le_log (hh z hz) H
  rw [hid z hz, log_lift t z ht hz] at HL
  have hm : Real.log (realMonomial a z) ≤ Real.log t := by nlinarith
  exact (Real.log_le_log_iff (realMonomial_pos a z hz) ht).mp hm

/-- The recognizer's nonpositive-exponent rule. -/
theorem realMonomial_convexOn_nonpositive (a : I → ℝ) (ha : ∀ i, a i ≤ 0) :
    ConvexOn ℝ positiveOrthant (realMonomial a) := by
  let d := 1 - ∑ i, a i
  have hd : 0 < d := by
    have hsum : ∑ i, a i ≤ 0 := Finset.sum_nonpos fun i _ ↦ ha i
    dsimp [d]; linarith
  apply realMonomial_convex_of_lift a (fun i ↦ -a i / d) (1 / d) (fun _ ↦ 1)
  · positivity
  · intro i; exact div_nonneg (neg_nonneg.mpr (ha i)) hd.le
  · rw [← Finset.sum_div, Finset.sum_neg_distrib]
    have H : (1 : ℝ) / d + -(∑ i, a i) / d = 1 := by
      rw [← add_div]; change d / d = 1; exact div_self hd.ne'
    exact H.le
  · intro x hx; norm_num
  · intro x y u v hu hv huv; simpa using huv.symm
  · intro x hx
    rw [Real.log_one, realMonomial_log a hx, Finset.mul_sum, ← Finset.sum_add_distrib]
    have H : ∀ i, (1 / d) * (a i * Real.log (x i)) +
        (-a i / d) * Real.log (x i) = 0 := by intro i; ring
    simp_rw [H]; simp

/-- The recognizer's single-positive-exponent rule. Zero exponents are retained. -/
theorem realMonomial_convexOn_one_positive (a : I → ℝ) (j : I)
    (hj : 0 < a j) (ha : ∀ i, i ≠ j → a i ≤ 0) (hs : 1 ≤ ∑ i, a i) :
    ConvexOn ℝ positiveOrthant (realMonomial a) := by
  classical
  let b := fun i ↦ if i = j then (0 : ℝ) else -a i / a j
  have hb : ∀ i, 0 ≤ b i := by
    intro i; by_cases h : i = j
    · simp [b, h]
    · simp only [b, if_neg h]; exact div_nonneg (neg_nonneg.mpr (ha i h)) hj.le
  have hcoef : ∀ i, a i / a j + b i = if i = j then 1 else 0 := by
    intro i; by_cases h : i = j
    · subst i; simp [b, hj.ne']
    · simp [b, h]; ring
  have hsum : (∑ i, a i) / a j + ∑ i, b i = 1 := by
    rw [Finset.sum_div, ← Finset.sum_add_distrib]
    simp_rw [hcoef]
    simp
  apply realMonomial_convex_of_lift a b (1 / a j) (fun x ↦ x j)
  · positivity
  · exact hb
  · have H := div_le_div_of_nonneg_right hs hj.le
    linarith
  · intro x hx; exact hx j
  · intro x y u v hu hv huv; rfl
  · intro x hx
    rw [realMonomial_log a hx, Finset.mul_sum, ← Finset.sum_add_distrib]
    have H : ∀ i, (1 / a j) * (a i * Real.log (x i)) + b i * Real.log (x i) =
        (if i = j then 1 else 0) * Real.log (x i) := by
      intro i; rw [← hcoef i]; ring
    simp_rw [H]
    simp

/-- The two sufficient convexity tests accepted by the recognizer. -/
theorem realMonomial_convex_recognition (a : I → ℝ)
    (ha : (∀ i, a i ≤ 0) ∨ ∃ j, 0 < a j ∧ (∀ i, i ≠ j → a i ≤ 0) ∧
      1 ≤ ∑ i, a i) : ConvexOn ℝ positiveOrthant (realMonomial a) := by
  rcases ha with ha | ⟨j, hj, hrest, hsum⟩
  · exact realMonomial_convexOn_nonpositive a ha
  · exact realMonomial_convexOn_one_positive a j hj hrest hsum

/-- If all nonzero exponents are positive, recognized convexity extends continuously
across zero coordinates; the zero exponent contributes one. -/
theorem realMonomial_convex_boundary (a : I → ℝ) (ha : ∀ i, 0 ≤ a i)
    (hrec : (∀ i, a i ≤ 0) ∨ ∃ j, 0 < a j ∧ (∀ i, i ≠ j → a i ≤ 0) ∧
      1 ≤ ∑ i, a i) : ConvexOn ℝ nonnegativeOrthant (realMonomial a) :=
  convexOn_nonnegativeOrthant_of_continuous (realMonomial a)
    (realMonomial_continuous a ha) (realMonomial_convex_recognition a hrec)

end CertifiedMinlp
