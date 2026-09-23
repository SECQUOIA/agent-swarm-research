import Mathlib

/-! Dyadic folding for the square on the unit interval.
The weighted sum is defined recursively and then identified with its finite
sum formula. The square error follows from an algebraic folding identity.
A global Lipschitz bound proves that relaxing each fold to its three linear
inequalities preserves the maximum of the weighted sum. -/

namespace QuadraticPrecision

noncomputable def fold (t : ℝ) : ℝ := min (2*t) (2*(1-t))
noncomputable def foldSum : ℕ → ℝ → ℝ
  | 0, _ => 0
  | n+1, t => (fold t + foldSum n (fold t))/4
noncomputable def foldApprox (n : ℕ) (t : ℝ) : ℝ := t - foldSum n t
noncomputable def foldError (n : ℕ) : ℝ := (1/4 : ℝ)^n / 4

theorem fold_mem {t : ℝ} (ht : t ∈ Set.Icc (0 : ℝ) 1) : fold t ∈ Set.Icc (0 : ℝ) 1 := by
  constructor
  · exact le_min (by linarith [ht.1]) (by linarith [ht.2])
  · unfold fold
    rcases le_total t (1/2 : ℝ) with h | h
    · exact (min_le_left _ _).trans (by linarith)
    · exact (min_le_right _ _).trans (by linarith)

theorem fold_abs_sub (a b : ℝ) : |fold a - fold b| ≤ 2*|a-b| := by
  unfold fold
  rcases le_total a (1/2 : ℝ) with ha | ha <;>
    rcases le_total b (1/2 : ℝ) with hb | hb
  all_goals
    simp only [min_def]
    split_ifs <;> rw [abs_le] <;> constructor <;>
      nlinarith [le_abs_self (a-b), neg_abs_le (a-b)]

theorem foldSum_abs_sub (n : ℕ) (a b : ℝ) : |foldSum n a - foldSum n b| ≤ |a-b| := by
  induction n generalizing a b with
  | zero => simp [foldSum]
  | succ n ih =>
    have hi := ih (fold a) (fold b)
    have hf := fold_abs_sub a b
    have hh := abs_add_le (fold a-fold b) (foldSum n (fold a)-foldSum n (fold b))
    simp only [foldSum]
    rw [← sub_div, abs_div, abs_of_pos (by norm_num : (0 : ℝ)<4)]
    apply (div_le_iff₀ (by norm_num : (0 : ℝ)<4)).2
    convert (show |(fold a-fold b)+(foldSum n (fold a)-foldSum n (fold b))| ≤
      |a-b| * 4 by linarith) using 1 <;> congr 1; ring

theorem fold_square_identity (t : ℝ) : t - fold t / 2 + (fold t)^2 / 4 = t^2 := by
  unfold fold
  rcases le_total (2*t) (2*(1-t)) with h | h
  · rw [min_eq_left h]; ring
  · rw [min_eq_right h]; ring

theorem foldApprox_error (n : ℕ) {t : ℝ} (ht : t ∈ Set.Icc (0 : ℝ) 1) :
    0 ≤ foldApprox n t - t^2 ∧ foldApprox n t - t^2 ≤ foldError n := by
  induction n generalizing t with
  | zero =>
    simp only [foldApprox, foldSum, sub_zero, foldError, pow_zero]
    constructor
    · nlinarith [ht.1, ht.2]
    · nlinarith [sq_nonneg (t-1/2)]
  | succ n ih =>
    have hi := ih (fold_mem ht)
    have he := fold_square_identity t
    have hr : foldApprox (n+1) t - t^2 = (foldApprox n (fold t) - (fold t)^2)/4 := by
      simp only [foldApprox, foldSum] at *
      linarith
    rw [hr]
    constructor
    · exact div_nonneg hi.1 (by norm_num)
    · unfold foldError at *
      have hp : (1 / 4 : ℝ) ^ (n+1) = (1/4 : ℝ)^n * (1/4) := pow_succ _ _
      rw [hp]
      linarith [hi.2]

/-- The `n` free real coordinates of the continuous lift. -/
def FoldFeasible : (n : ℕ) → ℝ → (Fin n → ℝ) → Prop
  | 0, _, _ => True
  | n+1, t, g => 0 ≤ g 0 ∧ g 0 ≤ 2*t ∧ g 0 ≤ 2*(1-t) ∧
      FoldFeasible n (g 0) (fun i => g i.succ)

noncomputable def foldObjective : (n : ℕ) → (Fin n → ℝ) → ℝ
  | 0, _ => 0
  | n+1, g => (g 0 + foldObjective n (fun i => g i.succ))/4

noncomputable def exactFold : (n : ℕ) → ℝ → (Fin n → ℝ)
  | 0, _ => Fin.elim0
  | n+1, t => Fin.cons (fold t) (exactFold n (fold t))

theorem exactFold_feasible (n : ℕ) {t : ℝ} (ht : t ∈ Set.Icc (0 : ℝ) 1) :
    FoldFeasible n t (exactFold n t) := by
  induction n generalizing t with
  | zero => trivial
  | succ n ih =>
    change 0 ≤ fold t ∧ fold t ≤ 2*t ∧ fold t ≤ 2*(1-t) ∧ _
    exact ⟨(fold_mem ht).1, min_le_left _ _, min_le_right _ _, ih (fold_mem ht)⟩

theorem exactFold_objective (n : ℕ) (t : ℝ) : foldObjective n (exactFold n t) = foldSum n t := by
  induction n generalizing t with
  | zero => rfl
  | succ n ih =>
    simpa [foldObjective, exactFold, foldSum] using
      congrArg (fun x : ℝ => (fold t+x)/4) (ih (fold t))

theorem foldObjective_le (n : ℕ) (t : ℝ) (g : Fin n → ℝ) (hg : FoldFeasible n t g) :
    foldObjective n g ≤ foldSum n t := by
  induction n generalizing t with
  | zero => exact le_rfl
  | succ n ih =>
    obtain ⟨h0, h1, h2, htail⟩ := hg
    have hgmax : g 0 ≤ fold t := le_min h1 h2
    have hi := ih (g 0) (fun i => g i.succ) htail
    have hl := foldSum_abs_sub n (g 0) (fold t)
    rw [abs_of_nonpos (sub_nonpos.mpr hgmax)] at hl
    have hh := le_abs_self (foldSum n (g 0)-foldSum n (fold t))
    simp only [foldObjective, foldSum]
    linarith

/-- An existential system of linear inequalities with only continuous variables. -/
def FoldEpigraph (n : ℕ) (t w : ℝ) : Prop :=
  ∃ g : Fin n → ℝ, FoldFeasible n t g ∧ t-foldObjective n g-foldError n ≤ w

theorem foldEpigraph_iff (n : ℕ) {t w : ℝ} (ht : t ∈ Set.Icc (0 : ℝ) 1) :
    FoldEpigraph n t w ↔ foldApprox n t-foldError n ≤ w := by
  constructor
  · rintro ⟨g, hg, hw⟩
    have := foldObjective_le n t g hg
    unfold foldApprox
    linarith
  · intro hw
    exact ⟨exactFold n t, exactFold_feasible n ht,
      by simpa [exactFold_objective, foldApprox] using hw⟩

theorem foldEpigraph_contains_square (n : ℕ) {t : ℝ} (ht : t ∈ Set.Icc (0 : ℝ) 1) :
    FoldEpigraph n t (t^2) := by
  rw [foldEpigraph_iff n ht]
  linarith [(foldApprox_error n ht).2]

theorem foldEpigraph_error (n : ℕ) {t w : ℝ} (ht : t ∈ Set.Icc (0 : ℝ) 1)
    (hw : FoldEpigraph n t w) : t^2-foldError n ≤ w := by
  rw [foldEpigraph_iff n ht] at hw
  linarith [(foldApprox_error n ht).1]

/-- Residuals of the three linear inequalities at every fold. -/
noncomputable def foldConstraints : (n : ℕ) → ℝ → (Fin n → ℝ) → List ℝ
  | 0, _, _ => []
  | n+1, t, g => [-g 0, g 0-2*t, g 0-2*(1-t)] ++
      foldConstraints n (g 0) (fun i => g i.succ)

theorem foldConstraints_length (n : ℕ) (t : ℝ) (g : Fin n → ℝ) :
    (foldConstraints n t g).length = 3*n := by
  induction n generalizing t with
  | zero => rfl
  | succ n ih => simp [foldConstraints, ih]; omega

theorem foldConstraints_nonpos_iff (n : ℕ) (t : ℝ) (g : Fin n → ℝ) :
    (∀ a ∈ foldConstraints n t g, a ≤ 0) ↔ FoldFeasible n t g := by
  induction n generalizing t with
  | zero => simp [foldConstraints, FoldFeasible]
  | succ n ih =>
    simp [foldConstraints, FoldFeasible, ih]

/-- The actual finite inequality list, including the epigraph inequality. -/
noncomputable def foldEpigraphConstraints (n : ℕ) (t w : ℝ) (g : Fin n → ℝ) : List ℝ :=
  (t-foldObjective n g-foldError n-w) :: foldConstraints n t g

theorem foldEpigraphConstraints_length (n : ℕ) (t w : ℝ) (g : Fin n → ℝ) :
    (foldEpigraphConstraints n t w g).length = 3*n+1 := by
  simp [foldEpigraphConstraints, foldConstraints_length]

theorem foldEpigraphConstraints_iff (n : ℕ) (t w : ℝ) :
    (∃ g, ∀ a ∈ foldEpigraphConstraints n t w g, a ≤ 0) ↔ FoldEpigraph n t w := by
  simp only [foldEpigraphConstraints, List.mem_cons, forall_eq_or_imp,
    foldConstraints_nonpos_iff, sub_nonpos, FoldEpigraph]
  exact exists_congr (fun _ => and_comm)

theorem foldObjective_add (n : ℕ) (g h : Fin n → ℝ) :
    foldObjective n (g+h) = foldObjective n g + foldObjective n h := by
  induction n with
  | zero => simp [foldObjective]
  | succ n ih =>
    simp only [foldObjective, Pi.add_apply]
    rw [show (fun i : Fin n => g i.succ+h i.succ) =
      (fun i : Fin n => g i.succ)+(fun i : Fin n => h i.succ) from rfl, ih]
    ring

theorem foldObjective_smul (n : ℕ) (c : ℝ) (g : Fin n → ℝ) :
    foldObjective n (c • g) = c * foldObjective n g := by
  induction n with
  | zero => simp [foldObjective]
  | succ n ih =>
    simp only [foldObjective, Pi.smul_apply, smul_eq_mul]
    rw [show (fun i : Fin n => c*g i.succ) = c • (fun i : Fin n => g i.succ) from rfl, ih]
    ring

theorem foldObjective_eq_sum (n : ℕ) (g : Fin n → ℝ) :
    foldObjective n g = ∑ i : Fin n, (1/4 : ℝ)^(i.val+1) * g i := by
  induction n with
  | zero => simp [foldObjective]
  | succ n ih =>
    rw [Fin.sum_univ_succ]
    simp only [foldObjective, ih, Fin.val_zero, zero_add, pow_one, Fin.val_succ]
    simp_rw [pow_succ (1/4 : ℝ) (_+1)]
    rw [show (∑ i : Fin n, (1/4 : ℝ)^(i.val+1) * (1/4) * g i.succ) =
      (∑ i : Fin n, (1/4 : ℝ)^(i.val+1) * g i.succ) * (1/4) by
        rw [Finset.sum_mul]; apply Finset.sum_congr rfl; intro i _; ring]
    ring

theorem exactFold_eq_iterate (n : ℕ) (t : ℝ) (i : Fin n) :
    exactFold n t i = fold^[i.val+1] t := by
  induction n generalizing t with
  | zero => exact Fin.elim0 i
  | succ n ih =>
    refine Fin.cases ?_ (fun j => ?_) i
    · simp [exactFold]
    · simp only [exactFold, Fin.cons_succ, ih, Fin.val_succ]
      exact (Function.iterate_succ_apply fold (j.val+1) t).symm

theorem foldSum_eq_sum (n : ℕ) (t : ℝ) :
    foldSum n t = ∑ i : Fin n, (1/4 : ℝ)^(i.val+1) * fold^[i.val+1] t := by
  rw [← exactFold_objective, foldObjective_eq_sum]
  simp only [exactFold_eq_iterate]

theorem foldError_succ (n : ℕ) : foldError (n+1) = (1/2 : ℝ)^(2*n+4) := by
  unfold foldError
  rw [pow_add (1/2 : ℝ), pow_mul]
  norm_num
  rw [pow_succ]
  ring

/-- A direct linear-size bound for the explicit lift. -/
theorem foldEpigraph_size (n : ℕ) (t w : ℝ) (g : Fin n → ℝ) :
    Fintype.card (Fin n) = n ∧
    (foldEpigraphConstraints n t w g).length ≤ 3*(n+1) := by
  simp only [Fintype.card_fin, foldEpigraphConstraints_length, true_and]
  omega

end QuadraticPrecision
