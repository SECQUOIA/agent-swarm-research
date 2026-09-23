import Mathlib

/-!
# The QCPM potential on a fixed spatial domain

This file uses the affine slack and squared residual in arXiv:2311.03977v2.
Initialization is stated as the actual row equations `M * e + q = e`.
Suprema are over fixed domains, with boundedness or compactness explicit.
-/

namespace QipmFormal.QCPM
noncomputable section

open scoped BigOperators

abbrev Point (d : ℕ) := Fin d → ℝ

/-- The initial center is the vector of ones. -/
def initial (d : ℕ) : Point d := fun _ => 1

/-- Affine slack `s(z) = Mz + q`. -/
def slack {d : ℕ} (M : Fin d → Fin d → ℝ) (q z : Point d) : Point d :=
  fun i => (∑ j, M i j * z j) + q i

/-- Complementarity residual before subtracting the central parameter. -/
def complementarity {d : ℕ} (M : Fin d → Fin d → ℝ) (q z : Point d) : Point d :=
  fun i => z i * slack M q z i

/-- The QCPM potential `f_μ(z) = ‖F(z) - μe‖₂² / 2`. -/
def potential {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    (μ : ℝ) (z : Point d) : ℝ :=
  (∑ i, (complementarity M q z i - μ) ^ 2) / 2

/-- The initialization equations, without assuming the conclusion about `F`. -/
def Initialized {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d) : Prop :=
  ∀ i, (∑ j, M i j) + q i = 1

theorem slack_initial {d : ℕ} {M : Fin d → Fin d → ℝ} {q : Point d}
    (h : Initialized M q) : slack M q (initial d) = initial d := by
  funext i
  simpa [slack, initial] using h i

theorem complementarity_initial {d : ℕ} {M : Fin d → Fin d → ℝ} {q : Point d}
    (h : Initialized M q) : complementarity M q (initial d) = initial d := by
  funext i
  simp [complementarity, slack_initial h, initial]

theorem potential_at_initial {d : ℕ} {M : Fin d → Fin d → ℝ} {q : Point d}
    (h : Initialized M q) (μ : ℝ) :
    potential M q μ (initial d) = (d : ℝ) / 2 * (1 - μ) ^ 2 := by
  simp [potential, complementarity_initial h, initial]
  ring

theorem potential_nonneg {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    (μ : ℝ) (z : Point d) : 0 ≤ potential M q μ z := by
  exact div_nonneg (Finset.sum_nonneg fun _ _ => sq_nonneg _) (by norm_num)

theorem continuous_potential {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    (μ : ℝ) : Continuous (potential M q μ) := by
  unfold potential complementarity slack
  fun_prop

/-- The supremum cannot be replaced by a concentration estimate near a moving center. -/
theorem initial_value_le_sup {d : ℕ} {M : Fin d → Fin d → ℝ} {q : Point d}
    (h : Initialized M q) (μ : ℝ) {Ω : Set (Point d)}
    (he : initial d ∈ Ω) (hb : BddAbove (potential M q μ '' Ω)) :
    (d : ℝ) / 2 * (1 - μ) ^ 2 ≤ sSup (potential M q μ '' Ω) := by
  rw [← potential_at_initial h μ]
  exact le_csSup hb (Set.mem_image_of_mem _ he)

theorem initial_value_le_sup_of_compact {d : ℕ} {M : Fin d → Fin d → ℝ}
    {q : Point d} (h : Initialized M q) (μ : ℝ) {Ω : Set (Point d)}
    (he : initial d ∈ Ω) (hΩ : IsCompact Ω) :
    (d : ℝ) / 2 * (1 - μ) ^ 2 ≤ sSup (potential M q μ '' Ω) :=
  initial_value_le_sup h μ he (hΩ.bddAbove_image (continuous_potential M q μ).continuousOn)

theorem initial_value_ge_dim_div_eight {d : ℕ} {M : Fin d → Fin d → ℝ}
    {q : Point d} (h : Initialized M q) {μ : ℝ} (hμ : μ ≤ 1 / 2) :
    (d : ℝ) / 8 ≤ potential M q μ (initial d) := by
  rw [potential_at_initial h]
  have hd : (0 : ℝ) ≤ d := Nat.cast_nonneg _
  have hs : (1 / 2 : ℝ) ^ 2 ≤ (1 - μ) ^ 2 := by nlinarith
  nlinarith [mul_nonneg hd (sub_nonneg.mpr hs)]

/-- A proposed uniform coefficient must diverge at least quadratically. -/
theorem coefficient_lower_bound {d : ℕ} {M : Fin d → Fin d → ℝ} {q : Point d}
    (h : Initialized M q) {ε γ K : ℝ} (hε : 0 < ε) (hεhalf : ε ≤ 1 / 2)
    (hγ : 0 < γ) (hbound : potential M q ε (initial d) ≤ K * γ ^ 2 * ε ^ 2) :
    (d : ℝ) / (8 * γ ^ 2 * ε ^ 2) ≤ K := by
  apply (div_le_iff₀ (by positivity : 0 < 8 * γ ^ 2 * ε ^ 2)).2
  have := (initial_value_ge_dim_div_eight h hεhalf).trans hbound
  nlinarith

/-- An explicit small parameter invalidates every nonnegative fixed coefficient. -/
theorem uniform_bound_fails_at_small_parameter {d : ℕ} (hd : 0 < d)
    {M : Fin d → Fin d → ℝ} {q : Point d} (h : Initialized M q)
    {K γ ε : ℝ} (hK : 0 ≤ K) (hε : 0 < ε) (hεhalf : ε ≤ 1 / 2)
    (hεsmall : ε ≤ 1 / (16 * (K * γ ^ 2 + 1))) :
    K * γ ^ 2 * ε ^ 2 < potential M q ε (initial d) := by
  have hx : 0 ≤ K * γ ^ 2 := mul_nonneg hK (sq_nonneg _)
  have hden : 0 < 16 * (K * γ ^ 2 + 1) := by positivity
  have hmul := (le_div_iff₀ hden).mp hεsmall
  have hsq : ε ^ 2 ≤ ε := by nlinarith
  have hprod := mul_le_mul_of_nonneg_left hsq hx
  have hd' : (1 : ℝ) ≤ d := by exact_mod_cast hd
  have hlower := initial_value_ge_dim_div_eight h hεhalf
  nlinarith

theorem no_uniform_quadratic_bound {d : ℕ} (hd : 0 < d)
    {M : Fin d → Fin d → ℝ} {q : Point d} (h : Initialized M q)
    {K γ : ℝ} (hK : 0 ≤ K) :
    ¬ ∀ μ : ℝ, 0 < μ → μ ≤ 1 →
      potential M q μ (initial d) ≤ K * γ ^ 2 * μ ^ 2 := by
  intro hbound
  let ε : ℝ := min (1 / 2) (1 / (16 * (K * γ ^ 2 + 1)))
  have hε : 0 < ε := by dsimp [ε]; positivity
  have hhalf : ε ≤ 1 / 2 := min_le_left _ _
  have hsmall : ε ≤ 1 / (16 * (K * γ ^ 2 + 1)) := min_le_right _ _
  exact (not_le_of_gt (uniform_bound_fails_at_small_parameter hd h hK hε hhalf hsmall))
    (hbound ε hε (by linarith))

/-- The same contradiction applies to the spatial supremum on every fixed compact domain
containing the initial center. -/
theorem no_uniform_quadratic_sup_bound {d : ℕ} (hd : 0 < d)
    {M : Fin d → Fin d → ℝ} {q : Point d} (h : Initialized M q)
    {Ω : Set (Point d)} (he : initial d ∈ Ω) (hΩ : IsCompact Ω)
    {K γ : ℝ} (hK : 0 ≤ K) :
    ¬ ∀ μ : ℝ, 0 < μ → μ ≤ 1 →
      sSup (potential M q μ '' Ω) ≤ K * γ ^ 2 * μ ^ 2 := by
  intro hbound
  apply no_uniform_quadratic_bound (γ := γ) hd h hK
  intro μ hμ hμone
  have hi := initial_value_le_sup_of_compact h μ he hΩ
  rw [← potential_at_initial h μ] at hi
  exact hi.trans (hbound μ hμ hμone)

/-- A genuine central point has zero potential. -/
theorem potential_at_center {d : ℕ} {M : Fin d → Fin d → ℝ} {q z : Point d}
    {μ : ℝ} (hz : ∀ i, complementarity M q z i = μ) : potential M q μ z = 0 := by
  simp [potential, hz]

/-- The range of two function values forces half their separation after any scalar shift. -/
theorem half_range_le_shifted_sup {α : Type*} {f : α → ℝ} {Ω : Set α}
    {x y : α} (hx : x ∈ Ω) (hy : y ∈ Ω) (c : ℝ)
    (hb : BddAbove ((fun z => |f z - c|) '' Ω)) :
    |f x - f y| / 2 ≤ sSup ((fun z => |f z - c|) '' Ω) := by
  have hx' := le_csSup hb (Set.mem_image_of_mem (fun z => |f z - c|) hx)
  have hy' := le_csSup hb (Set.mem_image_of_mem (fun z => |f z - c|) hy)
  have ht := abs_sub_le (f x) c (f y)
  rw [abs_sub_comm c (f y)] at ht
  linarith

/-- A scalar phase cannot recover quadratic decay if the domain contains both centers. -/
theorem shifted_potential_sup_lower {d : ℕ} {M : Fin d → Fin d → ℝ}
    {q : Point d} (h : Initialized M q) {μ : ℝ} {Ω : Set (Point d)}
    (he : initial d ∈ Ω) {z : Point d} (hz : z ∈ Ω)
    (hcenter : ∀ i, complementarity M q z i = μ) (c : ℝ)
    (hb : BddAbove ((fun z => |potential M q μ z - c|) '' Ω)) :
    (d : ℝ) / 4 * (1 - μ) ^ 2 ≤
      sSup ((fun z => |potential M q μ z - c|) '' Ω) := by
  have hr := half_range_le_shifted_sup he hz c hb
  rw [potential_at_center hcenter, sub_zero,
    abs_of_nonneg (potential_nonneg M q μ (initial d)), potential_at_initial h] at hr
  linarith

/-- Joint continuity allows taking the spatial supremum on a fixed compact domain. -/
theorem continuous_potential_joint {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d) :
    Continuous (fun p : ℝ × Point d => potential M q p.1 p.2) := by
  unfold potential complementarity slack
  fun_prop

theorem continuous_potential_sup {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    {Ω : Set (Point d)} (hΩ : IsCompact Ω) :
    Continuous (fun μ => sSup (potential M q μ '' Ω)) :=
  hΩ.continuous_sSup (continuous_potential_joint M q)

/-- Maximum absolute row sum, using the sup norm on the finite vector of row sums. -/
def matrixRowSumNorm {d : ℕ} (M : Fin d → Fin d → ℝ) : ℝ :=
  ‖fun i => ∑ j, |M i j|‖

theorem row_sum_le_matrixRowSumNorm {d : ℕ} (M : Fin d → Fin d → ℝ) (i : Fin d) :
    (∑ j, |M i j|) ≤ matrixRowSumNorm M := by
  have h := norm_le_pi_norm (fun i => ∑ j, |M i j|) i
  have hn : 0 ≤ ∑ j, |M i j| := Finset.sum_nonneg fun _ _ => abs_nonneg _
  simpa only [Real.norm_eq_abs, abs_of_nonneg hn, matrixRowSumNorm] using h

/-- The global upper certificate uses the fixed box, not a concentration region. -/
def boxCertificate {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d) (D : ℝ) : ℝ :=
  (d : ℝ) / 2 * (D * (D * matrixRowSumNorm M + ‖q‖) + 1) ^ 2

theorem slack_abs_le_on_box {d : ℕ} (M : Fin d → Fin d → ℝ) (q z : Point d)
    {D : ℝ} (hD : 0 ≤ D) (hz : ∀ i, 0 ≤ z i ∧ z i ≤ D) (i : Fin d) :
    |slack M q z i| ≤ D * matrixRowSumNorm M + ‖q‖ := by
  have hq : |q i| ≤ ‖q‖ := by simpa only [Real.norm_eq_abs] using norm_le_pi_norm q i
  have hsum : (∑ j, |M i j * z j|) ≤ D * matrixRowSumNorm M := by
    calc
      (∑ j, |M i j * z j|) ≤ ∑ j, |M i j| * D := by
        apply Finset.sum_le_sum
        intro j _
        rw [abs_mul, abs_of_nonneg (hz j).1]
        exact mul_le_mul_of_nonneg_left (hz j).2 (abs_nonneg _)
      _ = (∑ j, |M i j|) * D := (Finset.sum_mul _ _ _).symm
      _ ≤ D * matrixRowSumNorm M := by
        simpa only [mul_comm] using
          mul_le_mul_of_nonneg_right (row_sum_le_matrixRowSumNorm M i) hD
  have habs := Finset.abs_sum_le_sum_abs (fun j => M i j * z j) Finset.univ
  exact (abs_add_le _ _).trans (add_le_add (habs.trans hsum) hq)

theorem potential_le_boxCertificate {d : ℕ} (M : Fin d → Fin d → ℝ) (q z : Point d)
    {D μ : ℝ} (hD : 0 ≤ D) (hz : ∀ i, 0 ≤ z i ∧ z i ≤ D)
    (hμ : 0 ≤ μ) (hμone : μ ≤ 1) : potential M q μ z ≤ boxCertificate M q D := by
  let B := D * (D * matrixRowSumNorm M + ‖q‖) + 1
  have hR : 0 ≤ matrixRowSumNorm M := norm_nonneg _
  have hB : 0 ≤ B := by dsimp [B]; positivity
  have hcoord : ∀ i, |complementarity M q z i - μ| ≤ B := by
    intro i
    have hs := slack_abs_le_on_box M q z hD hz i
    have hp : |complementarity M q z i| ≤ D * (D * matrixRowSumNorm M + ‖q‖) := by
      rw [complementarity, abs_mul, abs_of_nonneg (hz i).1]
      exact mul_le_mul (hz i).2 hs (abs_nonneg _) hD
    have ht := abs_sub (complementarity M q z i) μ
    rw [abs_of_nonneg hμ] at ht
    dsimp [B]
    linarith
  have hsq : ∀ i, (complementarity M q z i - μ) ^ 2 ≤ B ^ 2 := by
    intro i
    exact sq_le_sq.mpr (by simpa only [abs_of_nonneg hB] using hcoord i)
  have hsum := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) => hsq i)
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at hsum
  unfold potential boxCertificate
  dsimp [B] at hsum
  linarith

/-- A box certificate also bounds the actual supremum on any nonempty subdomain. -/
theorem potential_sup_le_boxCertificate {d : ℕ} (M : Fin d → Fin d → ℝ)
    (q : Point d) {D μ : ℝ} (hD : 0 ≤ D) {Ω : Set (Point d)} (hΩ : Ω.Nonempty)
    (hbox : ∀ z ∈ Ω, ∀ i, 0 ≤ z i ∧ z i ≤ D) (hμ : 0 ≤ μ) (hμone : μ ≤ 1) :
    sSup (potential M q μ '' Ω) ≤ boxCertificate M q D := by
  apply csSup_le (hΩ.image _)
  rintro _ ⟨z, hz, rfl⟩
  exact potential_le_boxCertificate M q z hD (hbox z hz) hμ hμone

end

end QipmFormal.QCPM
