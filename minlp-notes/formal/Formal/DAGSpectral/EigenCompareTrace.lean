import Formal.DAGSpectral.EigenCompare
import Formal.DAGSpectral.DyadicScaleBits
import Formal.DAGSpectral.MatrixArithmeticTrace

/-! Executable dyadic search with the rational primitive events returned by
its actual threshold calls. No worst-case surrogate replaces the execution trace. -/
namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

def eigenQuery (R : ℚ) (k t : ℕ) : ℚ := R * (2 * k + 1) / (2:ℚ) ^ (t + 1)

def eigenQueryTrace (R : ℚ) (k t : ℕ) : List ArithmeticEvent :=
  powerTwoTrace (t + 1) ++
    [(.mul,2,(k:ℚ)), (.add,2 * (k:ℚ),1),
      (.mul,R,2 * (k:ℚ) + 1), (.div,R * (2 * (k:ℚ) + 1),(2:ℚ) ^ (t + 1))]

theorem eigenQueryTrace_length (R : ℚ) (k t : ℕ) :
    (eigenQueryTrace R k t).length = t + 5 := by
  simp [eigenQueryTrace, powerTwoTrace_length]

def dyadicIndexWithTrace (testRun : ℚ → Bool × List ArithmeticEvent) (R : ℚ) :
    ℕ → ℕ × List ArithmeticEvent
  | 0 => (0, [])
  | t + 1 =>
    let prev := dyadicIndexWithTrace testRun R t
    let query := eigenQuery R prev.1 t
    let result := testRun query
    (if result.1 then 2 * prev.1 + 1 else 2 * prev.1,
      prev.2 ++ eigenQueryTrace R prev.1 t ++ result.2)

def dyadicExecutionTrace (testRun : ℚ → Bool × List ArithmeticEvent) (R : ℚ) :
    ℕ → List ArithmeticEvent
  | 0 => []
  | t + 1 =>
    let k := dyadicIndex (fun q => (testRun q).1) R t
    dyadicExecutionTrace testRun R t ++ eigenQueryTrace R k t ++ (testRun (eigenQuery R k t)).2

theorem dyadicIndexWithTrace_eq (testRun : ℚ → Bool × List ArithmeticEvent) (R : ℚ) (t : ℕ) :
    dyadicIndexWithTrace testRun R t =
      (dyadicIndex (fun q => (testRun q).1) R t, dyadicExecutionTrace testRun R t) := by
  induction t with
  | zero => rfl
  | succ t ih => simp only [dyadicIndexWithTrace, ih, dyadicIndex, dyadicExecutionTrace, eigenQuery]

theorem dyadicIndexWithTrace_value (testRun : ℚ → Bool × List ArithmeticEvent)
    (test : ℚ → Bool) (h : ∀ q, (testRun q).1 = test q) (R : ℚ) (t : ℕ) :
    (dyadicIndexWithTrace testRun R t).1 = dyadicIndex test R t := by
  rw [dyadicIndexWithTrace_eq]
  simp only [h]

theorem dyadicExecutionTrace_length (testRun : ℚ → Bool × List ArithmeticEvent)
    {N : ℕ} (hlen : ∀ q, ((testRun q).2).length ≤ N) (R : ℚ) (t : ℕ) :
    (dyadicExecutionTrace testRun R t).length ≤ t * (t + N + 5) := by
  induction t with
  | zero => simp [dyadicExecutionTrace]
  | succ t ih =>
    simp only [dyadicExecutionTrace, List.length_append, eigenQueryTrace_length]
    have ht := hlen (eigenQuery R (dyadicIndex (fun q => (testRun q).1) R t) t)
    nlinarith

theorem rationalBits_nat_of_lt_two_pow {k t : ℕ} (hk : k < 2 ^ t) :
    RationalBits (k : ℚ) (t + 1) := by
  unfold RationalBits
  simp only [Rat.num_natCast, Rat.den_natCast, Int.natAbs_natCast]
  constructor
  · exact hk.trans_le (Nat.pow_le_pow_right (by decide) (Nat.le_succ t))
  · exact Nat.one_lt_pow (by omega) (by decide)

theorem eigenQuery_bits {R : ℚ} {B k t : ℕ} (hR : RationalBits R B) (hk : k < 2 ^ t) :
    RationalBits (eigenQuery R k t) (B + 3 * t + 8) := by
  have hi := rationalBits_nat_of_lt_two_pow hk
  have hn := rationalBits_add (rationalBits_mul rationalBits_two hi) rationalBits_one
  have hp := rationalBits_div (rationalBits_mul hR hn) (rationalBits_two_pow (t + 1))
  apply rationalBits_mono hp
  omega

theorem eigenQueryTrace_bits {R : ℚ} {B k t : ℕ} (hR : RationalBits R B)
    (hk : k < 2 ^ t) : ∀ e ∈ eigenQueryTrace R k t, eventBits (B + 3 * t + 8) e := by
  have hi := rationalBits_nat_of_lt_two_pow hk
  have h2i := rationalBits_mul rationalBits_two hi
  have hn := rationalBits_add h2i rationalBits_one
  have hp := rationalBits_mul hR hn
  intro e he
  simp only [eigenQueryTrace, List.mem_append, List.mem_cons, List.not_mem_nil, or_false] at he
  rcases he with he | (rfl | rfl | rfl | rfl)
  · exact eventBits_mono (powerTwoTrace_bits (t + 1) e he) (by omega)
  · exact ⟨rationalBits_mono rationalBits_two (by omega), rationalBits_mono hi (by omega)⟩
  · exact ⟨rationalBits_mono h2i (by omega), rationalBits_mono rationalBits_one (by omega)⟩
  · exact ⟨rationalBits_mono hR (by omega), rationalBits_mono hn (by omega)⟩
  · exact ⟨rationalBits_mono hp (by omega),
      rationalBits_mono (rationalBits_two_pow (t + 1)) (by omega)⟩

theorem dyadicExecutionTrace_bits (testRun : ℚ → Bool × List ArithmeticEvent)
    {R : ℚ} {B T K : ℕ} (hR : RationalBits R B) (hK : B + 3 * T + 8 ≤ K)
    (htest : ∀ q, RationalBits q (B + 3 * T + 8) → ∀ e ∈ (testRun q).2, eventBits K e)
    {t : ℕ} (ht : t ≤ T) :
    ∀ e ∈ dyadicExecutionTrace testRun R t, eventBits K e := by
  induction t with
  | zero => simp [dyadicExecutionTrace]
  | succ t ih =>
    intro e he
    simp only [dyadicExecutionTrace, List.mem_append] at he
    rcases he with (he | he) | he
    · exact ih (by omega) e he
    · exact eventBits_mono
        (eigenQueryTrace_bits hR (dyadicIndex_lt _ _ t) e he) (by omega)
    · apply htest _ _ e he
      exact rationalBits_mono (eigenQuery_bits hR (dyadicIndex_lt _ _ t)) (by omega)

theorem dyadicExecutionTrace_bitWork (testRun : ℚ → Bool × List ArithmeticEvent)
    {R : ℚ} {B T K N : ℕ} (hR : RationalBits R B) (hK : B + 3 * T + 8 ≤ K)
    (hlen : ∀ q, ((testRun q).2).length ≤ N)
    (htest : ∀ q, RationalBits q (B + 3 * T + 8) → ∀ e ∈ (testRun q).2, eventBits K e) :
    traceBitWork K (dyadicExecutionTrace testRun R T) ≤
      T * (T + N + 5) * (256 * (K + 1) ^ 3) := by
  apply (traceBitWork_le (dyadicExecutionTrace_bits testRun hR hK htest le_rfl)).trans
  exact Nat.mul_le_mul_right _ (dyadicExecutionTrace_length testRun hlen R T)

end DAGSpectral
