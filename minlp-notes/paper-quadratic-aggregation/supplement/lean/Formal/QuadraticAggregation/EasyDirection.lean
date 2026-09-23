import Formal.QuadraticAggregation.Model

/-!
# A nonconstant convex aggregation excludes a full convex hull

The certificate direction uses no hyperplane-convexity or nonemptiness assumption.
A positive semidefinite aggregate has a convex strict sublevel set. Its nonzero
quadratic or linear part ensures that this set is proper.
-/

open Matrix

namespace QuadraticAggregation

private def matrixQuadratic {n : ℕ} (A : Matrix (Fin n) (Fin n) ℝ)
    (b : Fin n → ℝ) (c : ℝ) (x : Fin n → ℝ) : ℝ :=
  x ⬝ᵥ (A *ᵥ x) + 2 * (b ⬝ᵥ x) + c

private theorem matrixQuadratic_convex {n : ℕ} (A : Matrix (Fin n) (Fin n) ℝ)
    (b : Fin n → ℝ) (c : ℝ) (hA : A.PosSemidef) :
    ConvexOn ℝ Set.univ (matrixQuadratic A b c) := by
  refine ⟨convex_univ, ?_⟩
  intro x _ y _ s t hs ht hst
  have hnonneg : 0 ≤ (x - y) ⬝ᵥ (A *ᵥ (x - y)) := by
    simpa using hA.dotProduct_mulVec_nonneg (x - y)
  have hid : matrixQuadratic A b c (s • x + t • y) =
      s * matrixQuadratic A b c x + t * matrixQuadratic A b c y -
        s * t * ((x - y) ⬝ᵥ (A *ᵥ (x - y))) := by
    simp only [matrixQuadratic, Matrix.mulVec_add, Matrix.mulVec_smul,
      add_dotProduct, dotProduct_add, smul_dotProduct, dotProduct_smul,
      Matrix.mulVec_sub, sub_dotProduct, dotProduct_sub, smul_eq_mul]
    have ht' : t = 1 - s := by linarith
    rw [ht']
    ring
  rw [hid]
  simpa only [smul_eq_mul] using sub_le_self
    (s * matrixQuadratic A b c x + t * matrixQuadratic A b c y)
    (mul_nonneg (mul_nonneg hs ht) hnonneg)

private theorem matrixQuadratic_not_everywhere_negative {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℝ) (b : Fin n → ℝ) (c : ℝ)
    (hA : A.PosSemidef) (hab : A ≠ 0 ∨ b ≠ 0) :
    ¬ ∀ x, matrixQuadratic A b c x < 0 := by
  intro hall
  have hc : c < 0 := by simpa [matrixQuadratic] using hall 0
  have hquad (x : Fin n → ℝ) : 0 ≤ x ⬝ᵥ (A *ᵥ x) := by
    simpa using hA.dotProduct_mulVec_nonneg x
  have hlin (x : Fin n → ℝ) : b ⬝ᵥ x = 0 := by
    by_contra hx
    let t := (1 - c) / (2 * (b ⬝ᵥ x))
    have ht : 2 * (b ⬝ᵥ (t • x)) + c = 1 := by
      simp only [dotProduct_smul, smul_eq_mul]
      dsimp [t]
      field_simp
      nlinarith
    have h := hall (t • x)
    dsimp [matrixQuadratic] at h
    have hn := hquad (t • x)
    linarith
  have hb : b = 0 := by
    ext i
    simpa using hlin (Pi.single i 1)
  have hzero (x : Fin n → ℝ) : x ⬝ᵥ (A *ᵥ x) = 0 := by
    by_contra hx
    have hp : 0 < x ⬝ᵥ (A *ᵥ x) := lt_of_le_of_ne (hquad x) (Ne.symm hx)
    let a := x ⬝ᵥ (A *ᵥ x)
    let t := (1 - c) / a + 1
    have ha : 0 < a := hp
    have hta : t * a = 1 - c + a := by dsimp [t]; field_simp
    have ht : 1 < t := by dsimp [t]; exact lt_add_of_pos_left _ (div_pos (by linarith) ha)
    have h := hall (t • x)
    simp only [matrixQuadratic, hb, zero_dotProduct, mul_zero, add_zero,
      Matrix.mulVec_smul, smul_dotProduct, dotProduct_smul, smul_eq_mul] at h
    change t * (t * a) + c < 0 at h
    nlinarith [mul_pos (sub_pos.mpr ht) (show 0 < t * a by positivity)]
  have hAz : A = 0 := by
    apply Matrix.ext_iff_mulVec.mpr
    intro x
    simpa using (hA.dotProduct_mulVec_zero_iff x).mp (by simpa using hzero x)
  exact hab.elim (fun h => h hAz) (fun h => h hb)

/-- Any aggregation certificate forces the convex hull of the strict feasible
set to be a proper subset of the ambient space. No hidden-convexity hypothesis
is needed in this direction. -/
theorem System.Certificate.convexHull_ne_univ {n m : ℕ} {D : System n m}
    {w : Vec m} (hw : D.Certificate w) : convexHull ℝ D.feasible ≠ Set.univ := by
  obtain ⟨hw, hw0, hA, hab⟩ := hw
  let f := matrixQuadratic (D.aggA w) (D.aggB w) (D.aggC w)
  have hconv : Convex ℝ {x | f x < 0} := by
    simpa using (matrixQuadratic_convex (D.aggA w) (D.aggB w) (D.aggC w) hA).convex_lt 0
  have hsub : D.feasible ⊆ {x | f x < 0} := by
    intro x hx
    have h := D.agg_eval_neg hw hw0 hx
    rw [D.agg_eval] at h
    exact h
  have hhull := convexHull_min hsub hconv
  intro hall
  apply matrixQuadratic_not_everywhere_negative (D.aggA w) (D.aggB w) (D.aggC w) hA hab
  intro x
  exact hhull (hall.symm ▸ Set.mem_univ x)

end QuadraticAggregation
