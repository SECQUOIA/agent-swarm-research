import Mathlib

/-! A finite-dimensional inequality alternative proved by variable elimination. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators
universe u v

/-- Nonnegative cancellation certificates have nonnegative right-hand side. -/
def CertificateCondition {I : Type u} [Fintype I] {m : ℕ}
    (A : I → Fin m → ℝ) (b : I → ℝ) : Prop :=
  ∀ μ : I → ℝ, (∀ i, 0 ≤ μ i) →
    (∀ j, ∑ i, μ i * A i j = 0) → 0 ≤ ∑ i, μ i * b i

theorem lift_certificate_sum {I : Type u} {K : Type v} [Fintype I] [Fintype K]
    (μ : K → ℝ) (W : K → I → ℝ) (v : I → ℝ) :
    (∑ i, (∑ k, μ k * W k i) * v i) = ∑ k, μ k * (∑ i, W k i * v i) := by
  simp_rw [Finset.sum_mul, Finset.mul_sum, mul_assoc]
  exact Finset.sum_comm

/-- Pairwise compatibility suffices for two finite families of scalar bounds,
even when either family is empty. -/
theorem finite_interval_point {N : Type u} {P : Type v} [Finite N] [Finite P]
    (lower : N → ℝ) (upper : P → ℝ) (h : ∀ n p, lower n ≤ upper p) :
    ∃ t : ℝ, (∀ n, lower n ≤ t) ∧ ∀ p, t ≤ upper p := by
  classical
  let _ : Fintype N := Fintype.ofFinite N
  let _ : Fintype P := Fintype.ofFinite P
  by_cases hn : Nonempty N
  · let _ := hn
    refine ⟨Finset.univ.sup' Finset.univ_nonempty lower, ?_, ?_⟩
    · intro n
      exact Finset.le_sup' lower (Finset.mem_univ n)
    · intro p
      exact Finset.sup'_le _ _ (fun n _ => h n p)
  · by_cases hp : Nonempty P
    · let _ := hp
      refine ⟨Finset.univ.inf' Finset.univ_nonempty upper, ?_, ?_⟩
      · intro n
        exact False.elim (hn ⟨n⟩)
      · intro p
        exact Finset.inf'_le upper (Finset.mem_univ p)
    · exact ⟨0, fun n => False.elim (hn ⟨n⟩), fun p => False.elim (hp ⟨p⟩)⟩

/-- The constructive elimination argument does not assume boundedness or full dimension. -/
theorem farkas_sufficient (m : ℕ) :
    ∀ (I : Type u) [Fintype I] (A : I → Fin m → ℝ) (b : I → ℝ),
      CertificateCondition A b → ∃ x : Fin m → ℝ, ∀ i, ∑ j, A i j * x j ≤ b i := by
  induction m with
  | zero =>
    intro I _ A b h
    classical
    refine ⟨Fin.elim0, ?_⟩
    intro i
    have hb := h (fun k => if k = i then 1 else 0)
      (fun k => by split_ifs <;> norm_num) (fun j => Fin.elim0 j)
    simpa using hb
  | succ m ih =>
    intro I _ A b h
    classical
    let Z := {i : I // A i 0 = 0}
    let P := {i : I // 0 < A i 0}
    let N := {i : I // A i 0 < 0}
    let E := Z ⊕ (P × N)
    let W : E → I → ℝ := fun e i => match e with
      | .inl z => if i = z.val then 1 else 0
      | .inr pn => (if i = pn.1.val then -A pn.2.val 0 else 0) +
          (if i = pn.2.val then A pn.1.val 0 else 0)
    have hW : ∀ e i, 0 ≤ W e i := by
      intro e i
      cases e with
      | inl z => dsimp [W]; split_ifs <;> norm_num
      | inr pn =>
        have hp := pn.1.property
        have hn := pn.2.property
        dsimp [W]
        split_ifs <;> linarith
    have wz (z : Z) (v : I → ℝ) : (∑ i, W (.inl z) i * v i) = v z.val := by
      simp [W]
    have wp (p : P) (n : N) (v : I → ℝ) :
        (∑ i, W (.inr (p, n)) i * v i) = -A n.val 0 * v p.val + A p.val 0 * v n.val := by
      simp [W, add_mul, Finset.sum_add_distrib]
    have wzero (e : E) : ∑ i, W e i * A i 0 = 0 := by
      cases e with
      | inl z => rw [wz]; exact z.property
      | inr pn => rw [wp]; ring
    let A' : E → Fin m → ℝ := fun e j => ∑ i, W e i * A i j.succ
    let b' : E → ℝ := fun e => ∑ i, W e i * b i
    have he : CertificateCondition A' b' := by
      intro μ hμ hcancel
      let ν : I → ℝ := fun i => ∑ e, μ e * W e i
      have hν : ∀ i, 0 ≤ ν i := fun i =>
        Finset.sum_nonneg fun e _ => mul_nonneg (hμ e) (hW e i)
      have hνc : ∀ j, ∑ i, ν i * A i j = 0 := by
        intro j
        refine Fin.cases ?_ (fun j => ?_) j
        · rw [show (∑ i, ν i * A i 0) = ∑ e, μ e * (∑ i, W e i * A i 0) from
            lift_certificate_sum μ W (fun i => A i 0)]
          simp only [wzero, mul_zero, Finset.sum_const_zero]
        · exact (lift_certificate_sum μ W (fun i => A i j.succ)).trans (hcancel j)
      exact (lift_certificate_sum μ W b) ▸ h ν hν hνc
    obtain ⟨y, hy⟩ := ih E A' b' he
    let tail : I → ℝ := fun i => ∑ j, A i j.succ * y j
    have eval (e : E) : (∑ j, A' e j * y j) = ∑ i, W e i * tail i := by
      dsimp only [A', tail]
      simp_rw [Finset.sum_mul, Finset.mul_sum]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro i _
      apply Finset.sum_congr rfl
      intro j _
      ring
    have hz (z : Z) : tail z.val ≤ b z.val := by
      have hh := hy (.inl z)
      change (∑ j, A' (.inl z) j * y j) ≤ ∑ i, W (.inl z) i * b i at hh
      rw [eval (.inl z), wz, wz] at hh
      exact hh
    have hpair (p : P) (n : N) :
        (b n.val - tail n.val) / A n.val 0 ≤ (b p.val - tail p.val) / A p.val 0 := by
      have hh := hy (.inr (p, n))
      change (∑ j, A' (.inr (p, n)) j * y j) ≤ ∑ i, W (.inr (p, n)) i * b i at hh
      rw [eval (.inr (p, n)), wp, wp] at hh
      rw [div_le_iff_of_neg n.property, div_mul_eq_mul_div, div_le_iff₀ p.property]
      nlinarith
    obtain ⟨t, htN, htP⟩ := finite_interval_point
      (fun n : N => (b n.val - tail n.val) / A n.val 0)
      (fun p : P => (b p.val - tail p.val) / A p.val 0) (fun n p => hpair p n)
    refine ⟨Fin.cons t y, ?_⟩
    intro i
    rw [Fin.sum_univ_succ]
    change A i 0 * t + tail i ≤ b i
    by_cases h0 : A i 0 = 0
    · have hh := hz ⟨i, h0⟩
      simpa only [h0, zero_mul, zero_add] using hh
    · by_cases hp : 0 < A i 0
      · have hh := (le_div_iff₀ hp).mp (htP ⟨i, hp⟩)
        nlinarith
      · have hn : A i 0 < 0 := lt_of_le_of_ne (le_of_not_gt hp) h0
        have hh := (div_le_iff_of_neg hn).mp (htN ⟨i, hn⟩)
        nlinarith

theorem farkas_inequalities {I : Type u} [Fintype I] {m : ℕ}
    (A : I → Fin m → ℝ) (b : I → ℝ) :
    (∃ x : Fin m → ℝ, ∀ i, ∑ j, A i j * x j ≤ b i) ↔ CertificateCondition A b := by
  constructor
  · rintro ⟨x, hx⟩ μ hμ hc
    have hs := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) =>
      mul_le_mul_of_nonneg_left (hx i) (hμ i))
    have he : (∑ i, μ i * (∑ j, A i j * x j)) = 0 := by
      simp_rw [Finset.mul_sum, ← mul_assoc]
      rw [Finset.sum_comm]
      simp_rw [← Finset.sum_mul, hc, zero_mul]
      exact Finset.sum_const_zero
    simpa only [he] using hs
  · exact farkas_sufficient m I A b

end NetworkSimplex.Threshold
