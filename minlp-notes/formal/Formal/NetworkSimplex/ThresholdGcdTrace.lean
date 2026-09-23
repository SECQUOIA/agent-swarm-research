import Formal.ReciprocalAnchor.ManyEuclidCost

/-! Executable gcd normalization with an actual remainder-division counter. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators
open ReciprocalAnchor.ManyLeaf.BitCost

def gcdFold : (n : ℕ) → (Fin n → ℕ) → ℕ
  | 0, _ => 0
  | n + 1, v => Nat.gcd (v 0) (gcdFold n (fun i => v i.succ))

theorem dvd_gcdFold (n : ℕ) (v : Fin n → ℕ) (d : ℕ) :
    d ∣ gcdFold n v ↔ ∀ i, d ∣ v i := by
  induction n with
  | zero => simp [gcdFold]
  | succ n ih => simp [gcdFold, Nat.dvd_gcd_iff, ih, Fin.forall_fin_succ]

theorem gcdFold_eq (n : ℕ) (v : Fin n → ℕ) : gcdFold n v = Finset.univ.gcd v := by
  apply Nat.dvd_antisymm
  · apply Finset.dvd_gcd
    intro i _
    exact (dvd_gcdFold n v _).mp (dvd_refl _) i
  · apply (dvd_gcdFold n v _).mpr
    intro i
    exact Finset.gcd_dvd (Finset.mem_univ i)

def gcdTrace : (n : ℕ) → (Fin n → ℕ) → ℕ × ℕ
  | 0, _ => (0, 0)
  | n + 1, v =>
      let tail := gcdTrace n (fun i => v i.succ)
      let step := countedEuclid (v 0) tail.1
      (step.1, tail.2 + step.2)

theorem gcdTrace_value (n : ℕ) (v : Fin n → ℕ) : (gcdTrace n v).1 = Finset.univ.gcd v := by
  rw [← gcdFold_eq]
  induction n with
  | zero => rfl
  | succ n ih => simp only [gcdTrace, countedEuclid_gcd, ih, gcdFold]

theorem gcdFold_lt (n B : ℕ) (v : Fin n → ℕ) (hv : ∀ i, v i < 2 ^ B) :
    gcdFold n v < 2 ^ B := by
  induction n with
  | zero => exact pow_pos (by decide) _
  | succ n ih =>
    by_cases h0 : v 0 = 0
    · simpa only [gcdFold, h0, Nat.gcd_zero_left] using ih (fun i => v i.succ)
        (fun i => hv i.succ)
    · exact (Nat.gcd_le_left _ (Nat.pos_of_ne_zero h0)).trans_lt (hv 0)

theorem gcdTrace_cost (n B : ℕ) (v : Fin n → ℕ) (hv : ∀ i, v i < 2 ^ B) :
    (gcdTrace n v).2 ≤ 2 * B * n := by
  induction n with
  | zero => simp [gcdTrace]
  | succ n ih =>
    have ht := ih (fun i => v i.succ) (fun i => hv i.succ)
    have hb : (gcdTrace n (fun i => v i.succ)).1.size ≤ B := by
      rw [gcdTrace_value, ← gcdFold_eq]
      exact Nat.size_le.mpr (gcdFold_lt n B _ (fun i => hv i.succ))
    have hc := countedEuclid_cost_size (v 0) (gcdTrace n (fun i => v i.succ)).1
    simp only [gcdTrace]
    nlinarith

/-- Every recursive gcd accumulator is bounded by the width of its inputs. -/
theorem gcdTrace_value_lt (n B : ℕ) (v : Fin n → ℕ) (hv : ∀ i, v i < 2 ^ B) :
    (gcdTrace n v).1 < 2 ^ B := by
  rw [gcdTrace_value, ← gcdFold_eq]
  exact gcdFold_lt n B v hv

/-- Exact normalization quotients cannot enlarge an input numerator, including
Lean's total division convention when every cofactor is zero. -/
theorem normalization_quotient_lt {B v d : ℕ} (hv : v < 2 ^ B) :
    v / d < 2 ^ B := (Nat.div_le_self _ _).trans_lt hv

/-- Calls reachable in the actual Euclidean recursion, including the initial call. -/
inductive EuclidReachable (a b : ℕ) : ℕ → ℕ → Prop
  | initial : EuclidReachable a b a b
  | step {x y : ℕ} : EuclidReachable a b x y → y ≠ 0 →
      EuclidReachable a b y (x % y)

/-- Every dividend and divisor in every recursive call has the original width. -/
theorem euclidReachable_bits {a b x y B : ℕ} (ha : a < 2 ^ B) (hb : b < 2 ^ B)
    (h : EuclidReachable a b x y) : x < 2 ^ B ∧ y < 2 ^ B := by
  induction h with
  | initial => exact ⟨ha, hb⟩
  | step _ hy ih => exact ⟨ih.2, (Nat.mod_lt _ (Nat.pos_of_ne_zero hy)).trans ih.2⟩

/-- Every remainder and quotient produced by a visited division has the same bound. -/
theorem euclidReachable_division_bits {a b x y B : ℕ}
    (ha : a < 2 ^ B) (hb : b < 2 ^ B) (h : EuclidReachable a b x y) :
    x % y < 2 ^ B ∧ x / y < 2 ^ B := by
  have hh := euclidReachable_bits ha hb h
  exact ⟨(Nat.mod_le _ _).trans_lt hh.1, (Nat.div_le_self _ _).trans_lt hh.1⟩

end NetworkSimplex.Threshold
