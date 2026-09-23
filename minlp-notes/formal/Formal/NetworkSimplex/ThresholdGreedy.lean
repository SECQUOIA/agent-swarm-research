import Formal.ReciprocalAnchor.ManyRationalSize

/-! Executable rational allocation into capacities and arbitrary coordinate intervals. -/

namespace NetworkSimplex.Chain
open scoped BigOperators
open ReciprocalAnchor

/-- Fill coordinates in order. The charge counts one rational comparison for `min`
and one subtraction at each coordinate. -/
def greedyFill : {N : ℕ} → (Fin N → ℚ) → ℚ → (Fin N → ℚ) × ℕ
  | 0, _, _ => (Fin.elim0, 0)
  | _N + 1, c, r =>
      let v := min r (c 0)
      let rest := greedyFill (fun i => c i.succ) (r - v)
      (Fin.cases v rest.1, rest.2 + 2)

theorem greedyFill_charge {N : ℕ} (c : Fin N → ℚ) (r : ℚ) :
    (greedyFill c r).2 = 2 * N := by
  induction N generalizing r with
  | zero => rfl
  | succ N ih => simp only [greedyFill, ih]; omega

theorem greedyFill_spec {N : ℕ} (c : Fin N → ℚ) (r : ℚ)
    (hc : ∀ i, 0 ≤ c i) (hr : 0 ≤ r) (hrc : r ≤ ∑ i, c i) :
    (∀ i, 0 ≤ (greedyFill c r).1 i ∧ (greedyFill c r).1 i ≤ c i) ∧
      (∑ i, (greedyFill c r).1 i) = r := by
  induction N generalizing r with
  | zero =>
      have hr0 : r = 0 := by simpa using le_antisymm hrc hr
      exact ⟨fun i => Fin.elim0 i, by simp [hr0]⟩
  | succ N ih =>
      have hv0 : 0 ≤ min r (c 0) := le_min hr (hc 0)
      have hres0 : 0 ≤ r - min r (c 0) := sub_nonneg.mpr (min_le_left _ _)
      have hres : r - min r (c 0) ≤ ∑ i : Fin N, c i.succ := by
        rw [Fin.sum_univ_succ] at hrc
        have hsum : 0 ≤ ∑ i : Fin N, c i.succ := Finset.sum_nonneg fun i _ => hc i.succ
        rcases le_total r (c 0) with h | h
        · rw [min_eq_left h]; linarith
        · rw [min_eq_right h]; linarith
      obtain ⟨hb, hs⟩ := ih (fun i => c i.succ) (r - min r (c 0))
        (fun i => hc i.succ) hres0 hres
      constructor
      · intro i
        refine Fin.cases ?_ (fun j => ?_) i
        · exact ⟨hv0, min_le_right _ _⟩
        · exact hb j
      · simp only [greedyFill, Fin.sum_univ_succ, Fin.cases_zero, Fin.cases_succ]
        rw [hs]
        ring

private theorem residual_bits {r c : ℚ} {R B : ℕ}
    (hr : RationalBits r R) (hc : RationalBits c B) :
    RationalBits (r - min r c) (R + B + 1) := by
  rcases le_total r c with h | h
  · rw [min_eq_left h, sub_self]
    exact rationalBits_mono rationalBits_zero (by omega)
  · rw [min_eq_right h]
    exact rationalBits_sub hr hc

/-- Residuals at the successive recursive calls, including initial and final mass. -/
def greedyResiduals : {N : ℕ} → (Fin N → ℚ) → ℚ → Fin (N + 1) → ℚ
  | 0, _, r => fun _ => r
  | _N + 1, c, r =>
      Fin.cases r (greedyResiduals (fun i => c i.succ) (r - min r (c 0)))

theorem greedyResiduals_bits {N R B : ℕ} (c : Fin N → ℚ) (r : ℚ)
    (hc : ∀ i, RationalBits (c i) B) (hr : RationalBits r R) :
    ∀ i, RationalBits (greedyResiduals c r i) (R + i.val * (B + 1)) := by
  induction N generalizing R r with
  | zero =>
      intro i
      have hi : i.val = 0 := by omega
      simpa [greedyResiduals, hi] using hr
  | succ N ih =>
      intro i
      refine Fin.cases ?_ (fun j => ?_) i
      · simpa [greedyResiduals] using hr
      · have hj := ih (fun i => c i.succ) (r - min r (c 0))
          (fun i => hc i.succ) (residual_bits hr (hc 0)) j
        change RationalBits (greedyResiduals (fun i => c i.succ)
          (r - min r (c 0)) j) _
        convert hj using 1; simp only [Fin.val_succ]; ring

/-- Every emitted rational has polynomial size in the input sizes and coordinate count.
The bound also covers intermediate recursive residuals through `residual_bits`. -/
theorem greedyFill_bits {N R B : ℕ} (c : Fin N → ℚ) (r : ℚ)
    (hc : ∀ i, RationalBits (c i) B) (hr : RationalBits r R) :
    ∀ i, RationalBits ((greedyFill c r).1 i) (R + N * (B + 1)) := by
  induction N generalizing R r with
  | zero => exact fun i => Fin.elim0 i
  | succ N ih =>
      intro i
      refine Fin.cases ?_ (fun j => ?_) i
      · change RationalBits (min r (c 0)) _
        rcases le_total r (c 0) with h | h
        · rw [min_eq_left h]
          exact rationalBits_mono hr (by omega)
        · rw [min_eq_right h]
          apply rationalBits_mono (hc 0)
          have : B ≤ (N + 1) * (B + 1) := by nlinarith
          omega
      · have hi := ih (fun i => c i.succ) (r - min r (c 0))
          (fun i => hc i.succ) (residual_bits hr (hc 0)) j
        change RationalBits ((greedyFill (fun i => c i.succ) (r - min r (c 0))).1 j) _
        convert hi using 1; ring

/-- Shift arbitrary intervals to capacities and then restore their lower endpoints.
The charge includes the `N` capacity subtractions, the lower-bound sum,
the total subtraction, and the `N` output additions. -/
def intervalFill {N : ℕ} (l u : Fin N → ℚ) (total : ℚ) : (Fin N → ℚ) × ℕ :=
  let r := total - ∑ i, l i
  let filled := greedyFill (fun i => u i - l i) r
  (fun i => l i + filled.1 i, filled.2 + 3 * N + 1)

theorem intervalFill_charge {N : ℕ} (l u : Fin N → ℚ) (total : ℚ) :
    (intervalFill l u total).2 = 5 * N + 1 := by
  simp only [intervalFill, greedyFill_charge]
  ring

theorem intervalFill_spec {N : ℕ} (l u : Fin N → ℚ) (total : ℚ)
    (hlu : ∀ i, l i ≤ u i) (hlo : (∑ i, l i) ≤ total) (hhi : total ≤ ∑ i, u i) :
    (∀ i, l i ≤ (intervalFill l u total).1 i ∧ (intervalFill l u total).1 i ≤ u i) ∧
      (∑ i, (intervalFill l u total).1 i) = total := by
  have hc : ∀ i, 0 ≤ u i - l i := fun i => sub_nonneg.mpr (hlu i)
  have hres : total - ∑ i, l i ≤ ∑ i, (u i - l i) := by
    rw [Finset.sum_sub_distrib]
    linarith
  obtain ⟨hb, hs⟩ := greedyFill_spec (fun i => u i - l i) (total - ∑ i, l i)
    hc (sub_nonneg.mpr hlo) hres
  constructor
  · intro i
    change l i ≤ l i + _ ∧ l i + _ ≤ u i
    constructor <;> linarith [(hb i).1, (hb i).2]
  · simp only [intervalFill, Finset.sum_add_distrib]
    rw [hs]
    ring

theorem intervalFill_bits {N B : ℕ} (l u : Fin N → ℚ) (total : ℚ)
    (hl : ∀ i, RationalBits (l i) B) (hu : ∀ i, RationalBits (u i) B)
    (ht : RationalBits total B) :
    ∀ i, RationalBits ((intervalFill l u total).1 i)
      (2 * B + 3 + N * (3 * B + 3)) := by
  have hs := rationalBits_finset_sum Finset.univ l (fun i _ => hl i)
  simp only [Finset.card_univ, Fintype.card_fin] at hs
  have hr := rationalBits_sub ht hs
  have hc : ∀ i, RationalBits (u i - l i) (2 * B + 1) := by
    intro i
    convert rationalBits_sub (hu i) (hl i) using 1; omega
  intro i
  have hf := greedyFill_bits (fun i => u i - l i) (total - ∑ i, l i) hc hr i
  have hout := rationalBits_add (hl i) hf
  change RationalBits ((intervalFill l u total).1 i) _ at hout
  convert hout using 1; ring

end NetworkSimplex.Chain
