import Formal.NetworkSimplex.ThresholdBalancedAlgebra

/-! Actual common profiles for the balanced-incidence coordinate section. -/
namespace NetworkSimplex.Chain.Balanced
open scoped BigOperators
open StateClass
noncomputable section
variable {N : ℕ}

def pattern (S : Fin N → Finset (Fin N)) (i j : Fin N) : StateClass :=
  if j ∈ S i then .neither else .aOnly

def observed (a : ℝ) (r s jr js : Fin N) (u v : ℝ) (i j : Fin N) : ℝ :=
  a / 4 + (if i = r ∧ j = jr then u else 0) + (if i = s ∧ j = js then v else 0)

def aggregate (S : Fin N → Finset (Fin N)) (a : ℝ) (i : Fin N) : ℝ :=
  ∑ j, if j ∈ S i then a else a / 4

@[simp] theorem pattern_observesA (S : Fin N → Finset (Fin N)) (i j : Fin N) :
    observesA (pattern S i j) ↔ j ∉ S i := by
  unfold pattern observesA
  split_ifs <;> simp_all

@[simp] theorem pattern_not_b (S : Fin N → Finset (Fin N)) (i j : Fin N) :
    ¬ observesB (pattern S i j) := by
  unfold pattern observesB
  split_ifs <;> simp

@[simp] theorem pattern_bSum (S : Fin N → Finset (Fin N)) (w : Fin N → ℝ) (i : Fin N) :
    bSum (pattern S i) w = 0 := by
  unfold bSum
  apply Finset.sum_eq_zero
  intro j _
  by_cases hj : j ∈ S i <;> simp [pattern, hj]

@[simp] theorem pattern_free (S : Fin N → Finset (Fin N)) (w : Fin N → ℝ) (i j : Fin N) :
    freeA (pattern S i) w j = if j ∈ S i then w j else 0 := by
  unfold freeA pattern
  split_ifs <;> simp_all

theorem observed_sum (S : Fin N → Finset (Fin N)) (a : ℝ) (r s jr js : Fin N)
    (hr : jr ∉ S r) (hs : js ∉ S s) (u v : ℝ) (i : Fin N) :
    (∑ j, if j ∉ S i then observed a r s jr js u v i j else 0) =
      (∑ j, if j ∉ S i then a / 4 else 0) + delta r s u v i := by
  have he : ∀ j, (if j ∉ S i then observed a r s jr js u v i j else 0) =
      (if j ∉ S i then a / 4 else 0) +
        (if i = r ∧ j = jr then u else 0) + (if i = s ∧ j = js then v else 0) := by
    intro j
    by_cases hij : j ∈ S i
    · have hnr : ¬(i = r ∧ j = jr) := by rintro ⟨rfl, rfl⟩; exact hr hij
      have hns : ¬(i = s ∧ j = js) := by rintro ⟨rfl, rfl⟩; exact hs hij
      simp [hij, hnr, hns]
    · simp [hij, observed]
  simp_rw [he, Finset.sum_add_distrib]
  simp only [ite_and, Finset.sum_ite_irrel, Finset.sum_ite_eq', Finset.mem_univ, ↓reduceIte]
  simp [delta, add_assoc]

theorem pattern_residual (S : Fin N → Finset (Fin N)) (a : ℝ) (r s jr js : Fin N)
    (hr : jr ∉ S r) (hs : js ∉ S s) (u v : ℝ) (i : Fin N) :
    residual (pattern S i) (observed a r s jr js u v i) (fun _ => 0) (aggregate S a i) =
      (∑ j, if j ∈ S i then a else 0) - delta r s u v i := by
  unfold residual
  simp only [pattern_observesA, ite_self, Finset.sum_const_zero, add_zero]
  rw [observed_sum S a r s jr js hr hs]
  have he : aggregate S a i = (∑ j, if j ∈ S i then a else 0) +
      ∑ j, if j ∉ S i then a / 4 else 0 := by
    unfold aggregate
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j _
    split_ifs <;> simp_all
  rw [he]
  ring

/-- Each observed value stays strictly inside its prescribed small positive range. -/
theorem observed_bounds {a R C u v : ℝ} (ha : 0 < a) (hR : 0 < R) (hC : 0 ≤ C)
    (hu : |u| < epsilon a R C) (hv : |v| < epsilon a R C)
    {r s : Fin N} (hrs : r ≠ s) (jr js i j : Fin N) :
    0 < observed a r s jr js u v i j ∧ observed a r s jr js u v i j < a / 2 := by
  have hb : ∀ x : ℝ, |x| < epsilon a R C → |x| < a / 16 := by
    intro x hx
    have hc := epsilon_control ha hR hC hx
    nlinarith [abs_nonneg x, mul_nonneg hC (abs_nonneg x),
      mul_nonneg hR.le (abs_nonneg x), mul_nonneg (mul_nonneg hC hR.le) (abs_nonneg x)]
  have hub := abs_lt.mp (hb u hu)
  have hvb := abs_lt.mp (hb v hv)
  unfold observed
  split_ifs with hur hvs
  · exact False.elim (hrs (hur.1.symm.trans hvs.1))
  · constructor <;> linarith
  · constructor <;> linarith
  · constructor <;> linarith

theorem observed_nonnegative {a R C u v : ℝ} (ha : 0 < a) (hR : 0 < R) (hC : 0 ≤ C)
    (hu : |u| < epsilon a R C) (hv : |v| < epsilon a R C)
    (S : Fin N → Finset (Fin N)) {r s : Fin N} (hrs : r ≠ s) (jr js i : Fin N) :
    ObservedNonnegative (pattern S i) (observed a r s jr js u v i) (fun _ => 0) := by
  exact ⟨fun j _ => (observed_bounds ha hR hC hu hv hrs jr js i j).1.le,
    fun _ _ => le_rfl⟩

theorem matrix_deviation (S : Fin N → Finset (Fin N)) (w : Fin N → ℝ) (a : ℝ) (i : Fin N) :
    (incidenceMatrix S).mulVec (fun j => w j - a) i =
      (∑ j, if j ∈ S i then w j else 0) - ∑ j, if j ∈ S i then a else 0 := by
  simp only [Matrix.mulVec, dotProduct, incidenceMatrix, ite_mul, one_mul, zero_mul,
    ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro j _
  split_ifs <;> simp

/-- Necessity uses the genuine profile rows and the positive balancing vector. -/
theorem profile_necessary (S : Fin N → Finset (Fin N)) (alpha : Fin N → ℝ)
    (halpha : ∀ i, 0 < alpha i) {beta a : ℝ} (hscale : (N : ℝ) * a = 1 / 2)
    (hbal : ∀ j, ∑ i, alpha i * incidenceMatrix S i j = beta)
    (r s jr js : Fin N) (hr : jr ∉ S r) (hs : js ∉ S s) (u v : ℝ)
    {w : Fin N → ℝ}
    (hp : Profile (pattern S) (observed a r s jr js u v) (fun _ _ => 0)
      (fun _ => 2 * a) (aggregate S a) (1 / 2) (fun _ => False) (fun _ => 0) w) :
    0 ≤ alpha r * u + alpha s * v := by
  have hrow : ∀ i, -delta r s u v i ≤ (incidenceMatrix S).mulVec (fun j => w j - a) i := by
    intro i
    have hi := (hp.2.2.2 i).2.2.2.2
    rw [pattern_bSum, pattern_residual S a r s jr js hr hs] at hi
    simp only [zero_add, pattern_free] at hi
    rw [matrix_deviation]
    linarith
  have hw : ∑ j, (w j - a) = 0 := by
    rw [Finset.sum_sub_distrib]
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, hscale]
    linarith [hp.2.1]
  have hsum := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) =>
    mul_le_mul_of_nonneg_left (hrow i) (halpha i).le)
  have hleft : (∑ i, alpha i * (-delta r s u v i)) = -(alpha r * u + alpha s * v) := by
    simp [delta, mul_neg, mul_add, Finset.sum_add_distrib, mul_ite]
  have hright : (∑ i, alpha i * (incidenceMatrix S).mulVec (fun j => w j - a) i) = 0 := by
    simp only [Matrix.mulVec, dotProduct, Finset.mul_sum]
    rw [Finset.sum_comm]
    simp only [← mul_assoc, ← Finset.sum_mul, hbal, ← Finset.mul_sum, hw, mul_zero]
  rw [hleft, hright] at hsum
  linarith

/-- The inverse perturbation is an actual feasible common profile on the full local halfplane. -/
theorem profile_sufficient (S : Fin N → Finset (Fin N)) (hK : IsUnit (incidenceMatrix S).det)
    (hne : ∀ i, (S i).Nonempty) (alpha : Fin N → ℝ) (halpha : ∀ i, 0 < alpha i)
    {beta a u v : ℝ} (hbeta : 0 < beta) (ha : 0 < a) (hscale : (N : ℝ) * a = 1 / 2)
    (hbal : ∀ j, ∑ i, alpha i * incidenceMatrix S i j = beta)
    {r s : Fin N} (hrs : r ≠ s) (jr js : Fin N) (hr : jr ∉ S r) (hs : js ∉ S s)
    (hu : |u| < epsilon a (alpha r / alpha s) (inverseSize (incidenceMatrix S)))
    (hv : |v| < epsilon a (alpha r / alpha s) (inverseSize (incidenceMatrix S)))
    (hh : 0 ≤ alpha r * u + alpha s * v) :
    Profile (pattern S) (observed a r s jr js u v) (fun _ _ => 0)
      (fun _ => 2 * a) (aggregate S a) (1 / 2) (fun _ => False) (fun _ => 0)
      (fun j => a + perturbation (incidenceMatrix S) r s (alpha r / alpha s) u v j) := by
  let R := alpha r / alpha s
  let d := perturbation (incidenceMatrix S) r s R u v
  have hR : 0 < R := div_pos (halpha r) (halpha s)
  have hd : ∀ j, |d j| < a / 16 := perturbation_bound hrs ha hR hu
  have hhh : 0 ≤ R * u + v := by
    apply nonneg_of_mul_nonneg_left (b := alpha s)
    · have heq : alpha s * (R * u + v) = alpha r * u + alpha s * v := by
        dsimp [R]
        field_simp [ne_of_gt (halpha s)]
      rw [mul_comm, heq]
      exact hh
    · exact halpha s
  have ht := tau_bound ha hR (norm_nonneg _) hu hv hhh
  have hdtotal := perturbation_sum_zero (incidenceMatrix S) hK alpha hbeta hbal hrs
    (ne_of_gt (halpha s)) u v
  have he := perturbation_equation (incidenceMatrix S) hK r s R u v
  have hob := fun i j => observed_bounds ha hR (norm_nonneg _) hu hv hrs jr js i j
  have hsmall : ∀ x : ℝ, |x| < epsilon a R (inverseSize (incidenceMatrix S)) → |x| < a / 16 := by
    intro x hx
    have hc := epsilon_control ha hR (norm_nonneg _) hx
    have hC : 0 ≤ inverseSize (incidenceMatrix S) := norm_nonneg _
    change (1 + inverseSize (incidenceMatrix S)) * (1 + R) * |x| < a / 16 at hc
    nlinarith [abs_nonneg x, mul_nonneg hC (abs_nonneg x),
      mul_nonneg hR.le (abs_nonneg x), mul_nonneg (mul_nonneg hC hR.le) (abs_nonneg x)]
  have hdelta : ∀ i, delta r s u v i < a / 16 := by
    intro i
    unfold delta
    split_ifs with hir his
    · exact False.elim (hrs (hir.symm.trans his))
    · simpa only [add_zero] using (le_abs_self u).trans_lt (hsmall u hu)
    · simpa only [zero_add] using (le_abs_self v).trans_lt (hsmall v hv)
    · linarith
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro j
    have hj := abs_lt.mp (hd j)
    change 0 ≤ a + d j ∧ a + d j ≤ 2 * a
    constructor <;> linarith
  · simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul, hdtotal, hscale]
    norm_num
  · intro j hj
    exact hj.elim
  · intro i
    refine ⟨?_, ?_, ?_, ?_, ?_⟩
    · intro j _
      have hj := abs_lt.mp (hd j)
      have ho := (hob i j).2
      change observed a r s jr js u v i j ≤ a + d j
      linarith
    · intro j hj
      unfold pattern at hj
      split_ifs at hj
    · intro j hj
      unfold pattern at hj
      split_ifs at hj
    · rw [pattern_bSum, pattern_residual S a r s jr js hr hs]
      obtain ⟨j, hj⟩ := hne i
      have hsum : a ≤ ∑ l : Fin N, if l ∈ S i then a else 0 := by
        simpa [hj] using Finset.single_le_sum
          (fun l (_ : l ∈ Finset.univ) => (show 0 ≤ (if l ∈ S i then a else 0) by positivity))
          (Finset.mem_univ j)
      linarith [hdelta i]
    · rw [pattern_bSum, pattern_residual S a r s jr js hr hs]
      simp only [zero_add, pattern_free]
      have hei := congrFun he i
      have ht0 : 0 ≤ tau s R u v i := by unfold tau; split_ifs <;> linarith [ht.1]
      have hsum : (∑ j : Fin N, if j ∈ S i then a + d j else 0) =
          (∑ j, if j ∈ S i then a else 0) + (incidenceMatrix S).mulVec d i := by
        simp only [Matrix.mulVec, dotProduct, incidenceMatrix, ite_mul, one_mul, zero_mul,
          ← Finset.sum_add_distrib]
        apply Finset.sum_congr rfl
        intro j _
        split_ifs <;> simp
      change (∑ j, if j ∈ S i then a else 0) - delta r s u v i ≤
        ∑ j, if j ∈ S i then a + d j else 0
      rw [hsum]
      change (incidenceMatrix S).mulVec d i = _ at hei
      linarith

/-- Start each unobserved cell at its common-profile upper bound. -/
def initialEntry (S : Fin N → Finset (Fin N)) (a : ℝ) (r s jr js : Fin N)
    (u v : ℝ) (d : Fin N → ℝ) (i j : Fin N) : ℝ :=
  if j ∈ S i then a + d j else observed a r s jr js u v i j

/-- The inverse equation gives precisely the row excess corrected in the paper. -/
theorem initialEntry_sum (S : Fin N → Finset (Fin N)) (a : ℝ) (r s jr js : Fin N)
    (hr : jr ∉ S r) (hs : js ∉ S s) (u v : ℝ) (d t : Fin N → ℝ)
    (he : (incidenceMatrix S).mulVec d = fun i => -delta r s u v i + t i) (i : Fin N) :
    ∑ j, initialEntry S a r s jr js u v d i j = aggregate S a i + t i := by
  have hsplit : (∑ j, initialEntry S a r s jr js u v d i j) =
      (∑ j, if j ∈ S i then a else 0) + (incidenceMatrix S).mulVec d i +
        ∑ j, if j ∉ S i then observed a r s jr js u v i j else 0 := by
    simp only [Matrix.mulVec, dotProduct, incidenceMatrix, ite_mul, one_mul, zero_mul,
      ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j _
    by_cases hj : j ∈ S i <;> simp [initialEntry, hj]
  rw [hsplit, observed_sum S a r s jr js hr hs, congrFun he i]
  have hag : (∑ j, if j ∈ S i then a else 0) +
      (∑ j, if j ∉ S i then a / 4 else 0) = aggregate S a i := by
    rw [← Finset.sum_add_distrib]
    unfold aggregate
    apply Finset.sum_congr rfl
    intro j _
    by_cases hj : j ∈ S i <;> simp [hj]
  linarith

/-- Subtracting the nonnegative excess from one unobserved cell preserves all
bounds and observations and gives the exact row aggregate. -/
theorem single_row_correction (S : Finset (Fin N)) (w z : Fin N → ℝ)
    (j₀ : Fin N) (hj₀ : j₀ ∈ S) {t X : ℝ} (ht : 0 ≤ t) (htw : t ≤ w j₀)
    (hw : ∀ j, 0 ≤ w j) (hz : ∀ j ∉ S, 0 ≤ z j ∧ z j ≤ w j)
    (hsum : (∑ j, if j ∈ S then w j else z j) = X + t) :
    let f := fun j => (if j ∈ S then w j else z j) - (if j = j₀ then t else 0)
    (∀ j, 0 ≤ f j ∧ f j ≤ w j) ∧ (∀ j ∉ S, f j = z j) ∧ ∑ j, f j = X := by
  dsimp only
  refine ⟨?_, ?_, ?_⟩
  · intro j
    by_cases he : j = j₀
    · subst j
      simp only [hj₀, ↓reduceIte]
      constructor <;> linarith
    · by_cases hj : j ∈ S
      · simp [he, hj, hw j]
      · simpa [he, hj] using hz j hj
  · intro j hj
    have he : j ≠ j₀ := by rintro rfl; exact hj hj₀
    simp [hj, he]
  · rw [Finset.sum_sub_distrib, hsum]
    simp

/-- The published perturbation margins allow the displayed single-cell correction. -/
theorem correction_margin {a T d : ℝ} (ha : 0 < a)
    (hd : |d| < a / 16) (hT : T < a / 16) : T < a + d := by
  have hh := (abs_lt.mp hd).1
  linarith

end
end NetworkSimplex.Chain.Balanced
