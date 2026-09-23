import Formal.QuadraticAggregation.Model

/-!
# Dines' convexity theorem

The joint image of two real quadratic forms is convex, including after restriction
to an arbitrary linear subspace. The proof uses a real root of a quadratic to
find two collinear images whose sum is a positive multiple of the desired image.
-/

namespace QuadraticAggregation

private theorem dines_root (c d : ℝ) : ∃ t : ℝ, c * (1 - t ^ 2) + d * t = 0 := by
  by_cases hc : c = 0
  · exact ⟨0, by simp [hc]⟩
  have hd : 0 ≤ discrim (-c) d c := by
    unfold discrim
    nlinarith [sq_nonneg d, sq_nonneg c]
  obtain ⟨t, ht⟩ := exists_quadratic_eq_zero (neg_ne_zero.mpr hc)
    ⟨Real.sqrt (discrim (-c) d c), by simpa [sq] using (Real.sq_sqrt hd).symm⟩
  exact ⟨t, by nlinarith [ht]⟩

private theorem dines_collinear {u T : Fin 2 → ℝ} (hT : T ≠ 0)
    (h : u 0 * T 1 - u 1 * T 0 = 0) : ∃ a : ℝ, u = a • T := by
  by_cases h0 : T 0 = 0
  · have h1 : T 1 ≠ 0 := by
      intro h1
      apply hT
      ext i
      fin_cases i <;> simp [h0, h1]
    refine ⟨u 1 / T 1, ?_⟩
    ext i
    fin_cases i
    · change u 0 = u 1 / T 1 * T 0
      rw [h0, mul_zero]
      exact (mul_eq_zero.mp (by simpa [h0] using h)).resolve_right h1
    · simp [h1]
  · refine ⟨u 0 / T 0, ?_⟩
    ext i
    fin_cases i
    · simp [h0]
    · change u 1 = u 0 / T 0 * T 1
      field_simp
      nlinarith [h]

private theorem dines_positive_ray {u v T : Fin 2 → ℝ} {k : ℝ}
    (hT : T ≠ 0) (hk : 0 < k) (hsum : u + v = k • T)
    (hdet : u 0 * T 1 - u 1 * T 0 = 0) :
    ∃ a : ℝ, 0 < a ∧ (u = a • T ∨ v = a • T) := by
  obtain ⟨a, ha⟩ := dines_collinear hT hdet
  by_cases hpos : 0 < a
  · exact ⟨a, hpos, Or.inl ha⟩
  · refine ⟨k - a, by linarith, Or.inr ?_⟩
    rw [ha] at hsum
    ext i
    have hi := congrFun hsum i
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul] at hi ⊢
    nlinarith

/-- The joint image of two quadratic forms on a real vector space is convex.
The two algebraic hypotheses are the homogeneity and polarization identities;
no topological or dimension hypothesis on the domain is needed. -/
theorem convex_image_quadratic_pair {V : Type*} [AddCommGroup V] [Module ℝ V]
    (Q : V → Fin 2 → ℝ)
    (hscale : ∀ (x : V) (t : ℝ), Q (t • x) = t ^ 2 • Q x)
    (hexpand : ∀ (x y : V) (a b : ℝ),
      Q (a • x + b • y) = a ^ 2 • Q x +
        (a * b) • (Q (x + y) - Q x - Q y) + b ^ 2 • Q y)
    (S : Submodule ℝ V) : Convex ℝ (Q '' (S : Set V)) := by
  have hzero : Q 0 = 0 := by simpa using hscale (0 : V) 0
  have hmul : ∀ {x : V}, x ∈ S → ∀ {a : ℝ}, 0 ≤ a →
      a • Q x ∈ Q '' (S : Set V) := by
    intro x hx a ha
    refine ⟨Real.sqrt a • x, S.smul_mem _ hx, ?_⟩
    rw [hscale, Real.sq_sqrt ha]
  have hadd : ∀ {x y : V}, x ∈ S → y ∈ S →
      Q x + Q y ∈ Q '' (S : Set V) := by
    intro x y hx hy
    let T := Q x + Q y
    by_cases hT : T = 0
    · exact ⟨0, S.zero_mem, by simpa [T] using hzero.trans hT.symm⟩
    let C := Q (x + y) - Q x - Q y
    obtain ⟨t, ht⟩ := dines_root
      (Q x 0 * T 1 - Q x 1 * T 0) (C 0 * T 1 - C 1 * T 0)
    let z := x + t • y
    let w := t • x - y
    have hz : z ∈ S := S.add_mem hx (S.smul_mem t hy)
    have hw : w ∈ S := S.sub_mem (S.smul_mem t hx) hy
    have hqz : Q z = Q x + t • C + t ^ 2 • Q y := by
      simpa [z, C] using hexpand x y 1 t
    have hqw : Q w = t ^ 2 • Q x + (-t) • C + Q y := by
      simpa [w, C, sub_eq_add_neg] using hexpand x y t (-1)
    have hsum : Q z + Q w = (1 + t ^ 2) • T := by
      rw [hqz, hqw]
      ext i
      simp only [T, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      ring
    have hdet : Q z 0 * T 1 - Q z 1 * T 0 = 0 := by
      rw [hqz]
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      dsimp [T] at ht ⊢
      nlinarith [ht]
    obtain ⟨a, ha, hza | hwa⟩ := dines_positive_ray hT (by positivity) hsum hdet
    · have hm := hmul hz (inv_nonneg.mpr ha.le)
      rw [hza, smul_smul, inv_mul_cancel₀ ha.ne', one_smul] at hm
      exact hm
    · have hm := hmul hw (inv_nonneg.mpr ha.le)
      rw [hwa, smul_smul, inv_mul_cancel₀ ha.ne', one_smul] at hm
      exact hm
  intro u hu v hv a b ha hb _
  obtain ⟨x, hx, rfl⟩ := hu
  obtain ⟨y, hy, rfl⟩ := hv
  obtain ⟨x', hx', hqx'⟩ := hmul hx ha
  obtain ⟨y', hy', hqy'⟩ := hmul hy hb
  rw [← hqx', ← hqy']
  exact hadd hx' hy'

/-- Dines' theorem for bundled quadratic maps with two real coordinates. -/
theorem QuadraticMap.convex_image_pair {V : Type*} [AddCommGroup V] [Module ℝ V]
    (Q : QuadraticMap ℝ V (Fin 2 → ℝ)) (S : Submodule ℝ V) :
    Convex ℝ (Q '' (S : Set V)) := by
  refine convex_image_quadratic_pair Q ?_ ?_ S
  · intro x t
    simpa [sq] using Q.map_smul t x
  · intro x y a b
    rw [QuadraticMap.map_add Q, Q.map_smul, Q.map_smul,
      Q.polar_smul_left, Q.polar_smul_right]
    simp only [QuadraticMap.polar, smul_smul, sq]
    abel

/-- Polarization identity for the homogenized quadratic system. -/
theorem System.homEval_combination {n m : ℕ} (D : System n m)
    (x y : Vec n × ℝ) (a b : ℝ) :
    D.homEval (a • x + b • y) = a ^ 2 • D.homEval x +
      (a * b) • (D.homEval (x + y) - D.homEval x - D.homEval y) +
      b ^ 2 • D.homEval y := by
  ext i
  simp only [System.homEval, Prod.fst_add, Prod.snd_add, Prod.smul_fst,
    Prod.smul_snd, q_add (D.A i) (D.symmetric i), q_smul,
    Matrix.mulVec_smul, dotProduct_smul, smul_dotProduct, dotProduct_add,
    Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  ring

/-- Every system of two real quadratic inequalities has hidden hyperplane convexity. -/
theorem System.hhc_pair {n : ℕ} (D : System n 2) : D.HHC := by
  intro l _
  exact convex_image_quadratic_pair D.homEval D.homEval_smul
    D.homEval_combination (LinearMap.ker l)

end QuadraticAggregation
