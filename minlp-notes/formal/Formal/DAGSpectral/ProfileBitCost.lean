import Formal.DAGSpectral.ProfileDPCost
import Formal.DAGSpectral.BitComplexity

namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

/-- Binary digit bound on the magnitude of a signed integer. -/
def IntegerBits (z : ℤ) (B : ℕ) : Prop := z.natAbs < 2^B

theorem integerBits_mono {z : ℤ} {B C : ℕ} (h : IntegerBits z B) (hBC : B ≤ C) :
    IntegerBits z C := h.trans_le (Nat.pow_le_pow_right (by decide) hBC)

theorem integerBits_add {x y : ℤ} {B : ℕ} (hx : IntegerBits x B)
    (hy : IntegerBits y B) : IntegerBits (x+y) (B+1) := by
  unfold IntegerBits at *
  have hh := Int.natAbs_add_le x y
  rw [pow_succ]
  omega

theorem integerBits_sum {xs : List ℤ} {B : ℕ} (h : ∀ x ∈ xs, IntegerBits x B) :
    IntegerBits xs.sum (B+xs.length) := by
  induction xs with
  | nil => simp [IntegerBits]
  | cons x xs ih =>
    have hx := integerBits_mono (h x (by simp)) (show B ≤ B+xs.length by omega)
    have hs := ih (fun y hy => h y (by simp [hy]))
    simpa [Nat.add_assoc] using integerBits_add hx hs

theorem rational_abs_bound {q : ℚ} {B : ℕ} (hq : RationalBits q B) :
    |q| < (2:ℚ)^B := by
  have hd : (0:ℚ) < q.den := by exact_mod_cast q.den_pos
  have hd1 : (1:ℚ) ≤ q.den := by exact_mod_cast q.den_pos
  have hn : |(q.num:ℚ)| < (2:ℚ)^B := by
    have h := hq.1
    have hh : (q.num.natAbs:ℚ) < (2:ℚ)^B := by exact_mod_cast h
    simpa only [Nat.cast_natAbs, Int.cast_abs] using hh
  rw [← Rat.num_div_den q,abs_div,abs_of_pos hd]
  apply (div_lt_iff₀ hd).2
  nlinarith [pow_pos (by norm_num : (0:ℚ)<2) B]

theorem integerBits_floor {q : ℚ} {B : ℕ} (hq : RationalBits q B) :
    IntegerBits ⌊q⌋ (B+1) := by
  obtain ⟨hlo,hhi⟩ := abs_lt.mp (rational_abs_bound hq)
  have hl : -(2^B:ℤ) ≤ ⌊q⌋ := Int.le_floor.mpr (by exact_mod_cast hlo.le)
  have hu : ⌊q⌋ ≤ (2^B:ℤ) := Int.floor_le_iff.mpr (by push_cast; linarith)
  have ha : (⌊q⌋:ℤ).natAbs ≤ 2^B := by
    have ha : |(⌊q⌋:ℤ)| ≤ (2^B:ℤ) := abs_le.mpr ⟨hl,hu⟩
    apply Int.ofNat_le.mp
    rw [Int.natCast_natAbs]
    simpa using ha
  unfold IntegerBits
  exact ha.trans_lt (by rw [pow_succ]; have := Nat.two_pow_pos B; omega)

/-- Signed division plus sign correction is a concrete schoolbook floor charge. -/
def rationalFloorBitCost (q : ℚ) : ℕ :=
  divisionCost q.num.natAbs.size q.den.size +
    3*addCost q.num.natAbs.size q.den.size

theorem rationalFloorBitCost_le {q : ℚ} {B : ℕ} (hq : RationalBits q B) :
    rationalFloorBitCost q ≤ 12*(B+1)^2 := by
  obtain ⟨hn,hd⟩ := (rationalBits_iff_size q B).mp hq
  have hv := divisionCost_mono hn hd
  have hm : max q.num.natAbs.size q.den.size ≤ B := max_le hn hd
  unfold rationalFloorBitCost
  simp only [divisionCost_eq,addCost] at *
  nlinarith

/-- The actual rational floor label includes both the ratio operation and the
signed floor operation. -/
def floorLabelBitWork (x h : ℚ) (B C : ℕ) : ℕ :=
  primitiveBitCost .div x h (max B C) + rationalFloorBitCost (x/h)

theorem floorLabelBitWork_le {x h : ℚ} {B C : ℕ}
    (hx : RationalBits x B) (hh : RationalBits h C) :
    floorLabelBitWork x h B C ≤ 268*(B+C+1)^3 := by
  have hdiv := primitiveBitCost_le (rationalBits_mono hx (le_max_left _ _))
    (rationalBits_mono hh (le_max_right _ _)) RationalPrimitive.div
  have hfloor := rationalFloorBitCost_le (rationalBits_div hx hh)
  have hm : max B C+1 ≤ B+C+1 := by omega
  have hp := Nat.pow_le_pow_left hm 3
  unfold floorLabelBitWork
  nlinarith [Nat.zero_le ((B+C+1)^2), Nat.zero_le ((B+C+1)^3),
    Nat.mul_self_le_mul_self (show 1 ≤ B+C+1 by omega)]

/-- Actual signed additions in a sequential sum, including intermediate sizes. -/
def integerSumBitWork : List ℤ → ℕ
  | [] => 0
  | x::xs => integerSumBitWork xs + addCost x.natAbs.size xs.sum.natAbs.size

theorem integerSumBitWork_le {xs : List ℤ} {B : ℕ}
    (h : ∀ x ∈ xs, IntegerBits x B) :
    integerSumBitWork xs ≤ xs.length*(B+xs.length+1) := by
  induction xs with
  | nil => simp [integerSumBitWork]
  | cons x xs ih =>
    have hx : x.natAbs.size ≤ B := Nat.size_le.mpr (h x (by simp))
    have hs : xs.sum.natAbs.size ≤ B+xs.length :=
      Nat.size_le.mpr (integerBits_sum (fun y hy => h y (by simp [hy])))
    have hm : max x.natAbs.size xs.sum.natAbs.size ≤ B+xs.length :=
      max_le (by omega) hs
    have ht := ih (fun y hy => h y (by simp [hy]))
    simp only [integerSumBitWork,addCost,List.length_cons]
    nlinarith

namespace ExplicitDAG
variable {v m : ℕ} {κ : Type*}

/-- Recomputed profile integers grow linearly in path length in their digit
bound. Rational denominator growth is not charged repeatedly along a path. -/
theorem profile_integerBits {label : Fin m → κ → ℤ} {B : ℕ}
    (hl : ∀ e i, IntegerBits (label e i) B) (es : List (Fin m)) (i : κ) :
    IntegerBits (profile label es i) (B+es.length) := by
  have h := integerBits_sum (xs := es.map (fun e => label e i))
    (by intro x hx; obtain ⟨e,_,rfl⟩ := List.mem_map.mp hx; exact hl e i)
  have he : (es.map (fun e => label e i)).sum = (es.map label).sum i := by
    clear h
    induction es with
    | nil => rfl
    | cons e es ih => simp [ih,Pi.add_apply]
  simpa [profile,he] using h

theorem path_profile_integerBits (G : ExplicitDAG v m) {s t : Fin v}
    {label : Fin m → κ → ℤ} {B : ℕ} (hl : ∀ e i, IntegerBits (label e i) B)
    {es : List (Fin m)} (hp : G.Path s t es) (i : κ) :
    IntegerBits (profile label es i) (B+v) :=
  integerBits_mono (profile_integerBits hl es i) (by have := hp.length_le_vertices; omega)

end ExplicitDAG
end DAGSpectral
