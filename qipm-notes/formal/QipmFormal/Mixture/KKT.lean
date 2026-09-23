import QipmFormal.Mixture.Residual
import QipmFormal.Mixture.Decoder

/-!
# Primal--dual mixtures

The dual multiplier is a signed real vector. Both blocks below are the actual
LP residuals, and the objective gap follows from feasibility, stationarity,
and coordinatewise complementarity.
-/
namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators

variable {I R C : Type*} [Fintype I] [Fintype R] [Fintype C]

def stationarity (A : R → C → ℝ) (y : R → ℝ) (s c : C → ℝ) : C → ℝ :=
  fun j => (∑ r, A r j * y r) + s j - c j

def kktSqResidual (A : R → C → ℝ) (b : R → ℝ) (c x : C → ℝ)
    (y : R → ℝ) (s : C → ℝ) : ℝ :=
  sqNorm (residual A x b) + sqNorm (stationarity A y s c)

theorem central_objective_gap (A : R → C → ℝ) (b y : R → ℝ)
    (c x s : C → ℝ) (μ : ℝ)
    (hp : ∀ r, ∑ j, A r j * x j = b r)
    (hd : ∀ j, (∑ r, A r j * y r) + s j = c j)
    (hc : ∀ j, x j * s j = μ) :
    dot c x - dot b y = (Fintype.card C : ℝ) * μ := by
  have h : dot c x = dot b y + ∑ j, x j * s j := by
    unfold dot
    simp_rw [← hd, add_mul, Finset.sum_add_distrib, Finset.sum_mul]
    rw [Finset.sum_comm]
    congr 1
    · apply Finset.sum_congr rfl
      intro r _
      rw [← hp r, Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro j _
      ring
    · apply Finset.sum_congr rfl
      intro j _
      ring
  rw [h]
  simp [hc]

theorem mixture_objective_gap (w : I → ℝ) (hw : ProbWeights w)
    (b : R → ℝ) (c : C → ℝ) (x : I → C → ℝ) (y : I → R → ℝ)
    (v : ℝ) (hgap : ∀ i, dot c (x i) - dot b (y i) = v) :
    dot c (mix w x) - dot b (mix w y) = v := by
  rw [dot_mix, dot_mix, ← Finset.sum_sub_distrib]
  simp_rw [← mul_sub, hgap]
  rw [← Finset.sum_mul, hw.2, one_mul]

theorem central_mixture_objective_gap (w : I → ℝ) (hw : ProbWeights w)
    (A : I → R → C → ℝ) (b : R → ℝ) (c : C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (μ : ℝ)
    (hp : ∀ i r, ∑ j, A i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A i r j * y i r) + s i j = c j)
    (hc : ∀ i j, x i j * s i j = μ) :
    dot c (mix w x) - dot b (mix w y) = (Fintype.card C : ℝ) * μ := by
  apply mixture_objective_gap w hw
  intro i
  exact central_objective_gap (A i) b (y i) c (x i) (s i) μ (hp i) (hd i) (hc i)

omit [Fintype C] in
theorem stationarity_mixture_identity (w : I → ℝ) (hw : ProbWeights w)
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (y : I → R → ℝ) (s : I → C → ℝ) (c : C → ℝ)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j) (j : C) :
    stationarity A (mix w y) (mix w s) c j =
      ∑ i, w i * (∑ r, (A r j - A' i r j) * y i r) := by
  have h : ∑ i, w i * c j = c j := by rw [← Finset.sum_mul, hw.2, one_mul]
  unfold stationarity mix
  simp only [Finset.mul_sum]
  rw [Finset.sum_comm, ← h, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rw [← hd i j]
  simp only [sub_mul]
  have hh : ∑ r, A r j * (w i * y i r) = ∑ r, w i * (A r j * y i r) := by
    apply Finset.sum_congr rfl
    intro r _
    ring
  rw [hh]
  simp only [mul_add, Finset.mul_sum, mul_sub, Finset.sum_sub_distrib]
  ring

/-- Dependent positions of the transpose, formed from the same raw positions. -/
def transposePositions [DecidableEq C] (D : R → Finset C) (j : C) : Finset R :=
  Finset.univ.filter fun r => j ∈ D r

theorem transpose_position_sum [DecidableEq C] (D : R → Finset C)
    (f : R → C → ℝ) :
    (∑ j, ∑ r ∈ transposePositions D j, f r j) = ∑ r, ∑ j ∈ D r, f r j := by
  classical
  simp only [transposePositions, Finset.sum_filter]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro r _
  rw [← Finset.sum_filter]
  simp

/-- Row and column sparsities control the two KKT blocks directly. This
    improves the split-multiplier constant and allows arbitrary signed duals. -/
theorem weighted_kkt_bound [DecidableEq I] [DecidableEq C]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (b : R → ℝ) (c : C → ℝ)
    (w : I → ℝ) (D : R → Finset C) (label : R → C → I)
    (sr sc : ℕ) (B H : ℝ) (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    kktSqResidual A b c (mix w x) (mix w y) (mix w s) ≤
      4 * (sr + sc : ℕ) * B ^ 2 * H ^ 2 *
        ∑ i, (incidence D label i : ℝ) * (w i)^2 := by
  classical
  have hpbound := weighted_residual_bound A A' x b w D label sr B H
    hw hB hH hA hA' hx hr hp hlocal
  have htlocal : ∀ i j r, r ∉ transposePositions D j ∨ label r j ≠ i →
      A' i r j = A r j := by
    intro i j r h
    apply hlocal
    simpa [transposePositions] using h
  have hdbound := matrixChangeMix_bound (fun j r => A r j)
    (fun i j r => A' i r j) y w (transposePositions D) (fun j r => label r j)
    sc B H hB hH (fun j r => hA r j) (fun i j r => hA' i r j)
    hy hcol htlocal
  have hdi : stationarity A (mix w y) (mix w s) c =
      matrixChangeMix (fun j r => A r j) (fun i j r => A' i r j) y w := by
    funext j
    rw [stationarity_mixture_identity w hw A A' y s c hd j]
    simp only [matrixChangeMix, Finset.mul_sum]
    exact Finset.sum_comm
  have hcost : (∑ i, (incidence (transposePositions D) (fun j r => label r j) i : ℝ) *
      (w i)^2) = ∑ i, (incidence D label i : ℝ) * (w i)^2 := by
    rw [← incidence_sum, ← incidence_sum]
    exact transpose_position_sum D (fun r j => (w (label r j))^2)
  rw [hcost, ← hdi] at hdbound
  unfold kktSqResidual
  have := add_le_add hpbound hdbound
  push_cast
  nlinarith

/-- The manuscript's split-stack constant follows from the sharper direct
    bound above, using its stated row/column sparsity and coefficient scales. -/
theorem weighted_kkt_paper_bound [DecidableEq I] [DecidableEq C]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (b : R → ℝ) (c : C → ℝ)
    (w : I → ℝ) (D : R → Finset C) (label : R → C → I)
    (sr sc : ℕ) (B H : ℝ) (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    kktSqResidual A b c (mix w x) (mix w y) (mix w s) ≤
      12 * (max sr (2 * sc + 1) : ℕ) * (max B 1) ^ 2 * H ^ 2 *
        ∑ i, (incidence D label i : ℝ) * (w i)^2 := by
  apply (weighted_kkt_bound A A' x s y b c w D label sr sc B H hw hB hH
    hA hA' hx hy hr hcol hp hd hlocal).trans
  have hs : sr + sc ≤ 3 * max sr (2 * sc + 1) := by
    have := le_max_left sr (2 * sc + 1)
    have := le_max_right sr (2 * sc + 1)
    omega
  have hs' : ((sr + sc : ℕ) : ℝ) ≤ 3 * (max sr (2 * sc + 1) : ℕ) := by
    exact_mod_cast hs
  have hb' : B^2 ≤ (max B 1)^2 := pow_le_pow_left₀ hB (le_max_left _ _) 2
  have hn : 0 ≤ ∑ i, (incidence D label i : ℝ) * (w i)^2 := by positivity
  have hscale : 4 * ((sr + sc : ℕ) : ℝ) ≤
      12 * (max sr (2 * sc + 1) : ℕ) := by linarith
  exact mul_le_mul_of_nonneg_right
    (mul_le_mul_of_nonneg_right
      (mul_le_mul hscale hb' (sq_nonneg B) (by positivity)) (sq_nonneg H)) hn

/-- The simultaneous primal--dual single-flip estimate in Euclidean norm. -/
theorem uniform_kkt_paper_bound [DecidableEq C] [Nonempty I]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (b : R → ℝ) (c : C → ℝ)
    (D : R → Finset C) (label : R → C → I)
    (sr sc : ℕ) (B H : ℝ) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    Real.sqrt (kktSqResidual A b c (mix (uniformWeight I) x)
      (mix (uniformWeight I) y) (mix (uniformWeight I) s)) ≤
      2 * max B 1 * H * Real.sqrt (3 * (max sr (2 * sc + 1) : ℕ) *
        totalIncidence D) / Fintype.card I := by
  classical
  have hn : (Fintype.card I : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr Fintype.card_pos)
  have hh := weighted_kkt_paper_bound A A' x s y b c (uniformWeight I) D label
    sr sc B H (uniformWeight_prob I) hB hH hA hA' hx hy hr hcol hp hd hlocal
  rw [← incidence_sum] at hh
  have hsum : (∑ r, ∑ j ∈ D r, (uniformWeight I (label r j)) ^ 2) =
      (totalIncidence D : ℝ) * ((Fintype.card I : ℝ)⁻¹) ^ 2 := by
    simp [uniformWeight, totalIncidence, Nat.cast_sum, Finset.sum_mul]
  rw [hsum] at hh
  apply Real.sqrt_le_iff.mpr
  constructor
  · positivity
  · have hr : Real.sqrt (3 * (max sr (2 * sc + 1) : ℕ) *
        totalIncidence D) ^ 2 = 3 * (max sr (2 * sc + 1) : ℕ) * totalIncidence D :=
      Real.sq_sqrt (by positivity)
    calc
      _ ≤ _ := hh
      _ = _ := by rw [div_pow, mul_pow, mul_pow, mul_pow, hr]; field_simp; ring

end
end QipmFormal.Mixture
