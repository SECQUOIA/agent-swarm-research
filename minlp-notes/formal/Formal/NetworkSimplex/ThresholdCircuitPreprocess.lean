import Formal.NetworkSimplex.ThresholdCircuitCandidates
import Formal.NetworkSimplex.ThresholdDetTrace
import Formal.NetworkSimplex.ThresholdGcdTrace

/-! Executable enumeration and checking of cofactor circuit certificates. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators

/-- Enumerate finite functions by their successive coordinate values. -/
def finiteFunctions : (k n : ℕ) → List (Fin k → Fin n)
  | 0, _ => [Fin.elim0]
  | k + 1, n => (List.finRange n).flatMap fun x =>
      (finiteFunctions k n).map (Fin.cons x)

theorem finiteFunctions_length (k n : ℕ) : (finiteFunctions k n).length = n ^ k := by
  induction k with
  | zero => simp [finiteFunctions]
  | succ k ih =>
    simp [finiteFunctions, List.length_flatMap, List.map_ofFn, List.finRange, ih,
      List.sum_ofFn, pow_succ, Nat.mul_comm]

theorem mem_finiteFunctions {k n : ℕ} (f : Fin k → Fin n) : f ∈ finiteFunctions k n := by
  induction k with
  | zero => simp [finiteFunctions, Subsingleton.elim f Fin.elim0]
  | succ k ih =>
    apply List.mem_flatMap.mpr
    refine ⟨f 0, by simp, List.mem_map.mpr ⟨fun i => f i.succ, ih _, ?_⟩⟩
    funext i
    exact Fin.cases rfl (fun _ => rfl) i

structure CofactorCandidate (m N : ℕ) where
  size : Fin (m + 1)
  support : Fin (size.val + 1) → Fin N
  columns : Fin size.val → Fin m

def cofactorCandidates (m N : ℕ) : List (CofactorCandidate m N) :=
  (List.finRange (m + 1)).flatMap fun s =>
    (finiteFunctions (s.val + 1) N).flatMap fun e =>
      (finiteFunctions s.val m).map fun f => ⟨s, e, f⟩

theorem mem_cofactorCandidates {m N : ℕ} (c : CofactorCandidate m N) :
    c ∈ cofactorCandidates m N := by
  apply List.mem_flatMap.mpr
  refine ⟨c.size, by simp, List.mem_flatMap.mpr ?_⟩
  refine ⟨c.support, mem_finiteFunctions _, List.mem_map.mpr ?_⟩
  exact ⟨c.columns, mem_finiteFunctions _, rfl⟩

namespace CofactorCandidate
variable {m N : ℕ}

def weights (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N) :
    Fin (c.size.val + 1) → ℕ :=
  primitiveWeights fun i => (cofactorVector (A.submatrix c.support c.columns) i).natAbs

/-- Positivity and cancellation are checked on all original coordinates. -/
def Valid (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N) : Prop :=
  (∀ i, 0 < c.weights A i) ∧ ∀ j, ∑ i, (c.weights A i : ℤ) * A (c.support i) j = 0

instance (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N) :
    Decidable (c.Valid A) := inferInstanceAs (Decidable (_ ∧ ∀ _, _))

theorem primitive (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N)
    (hc : c.Valid A) : Finset.univ.gcd (c.weights A) = 1 := by
  apply primitiveWeights_gcd
  refine ⟨0, ?_⟩
  have hp := hc.1 0
  have hb := primitiveWeights_le
    (fun i => (cofactorVector (A.submatrix c.support c.columns) i).natAbs) 0
  exact ne_of_gt (lt_of_lt_of_le hp hb)

theorem bounded (A : Matrix (Fin N) (Fin m) ℤ) (hA : RowSignedZeroOne A)
    (c : CofactorCandidate m N) (i : Fin (c.size.val + 1)) :
    c.weights A i ≤ delta01 m := by
  apply (primitiveWeights_le _ i).trans
  rw [cofactorVector_natAbs]
  exact ((hA.submatrix c.support c.columns).submatrix i.succAbove id).det_natAbs_le
    (by omega)

end CofactorCandidate

/-- Candidate generation, determinant evaluation, gcd normalization, and all
checks are executable integer operations. No existential certificate is chosen. -/
def preprocessCandidates {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) :
    List (CofactorCandidate m N) :=
  (cofactorCandidates m N).filter fun c => decide (c.Valid A)

theorem mem_preprocessCandidates {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (c : CofactorCandidate m N) : c ∈ preprocessCandidates A ↔ c.Valid A := by
  simp [preprocessCandidates, mem_cofactorCandidates]

theorem preprocessCandidates_sound {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) {c : CofactorCandidate m N} (hc : c ∈ preprocessCandidates A) :
    (∀ i, 0 < c.weights A i ∧ c.weights A i ≤ delta01 m) ∧
    Finset.univ.gcd (c.weights A) = 1 ∧
    ∀ j, ∑ i, (c.weights A i : ℤ) * A (c.support i) j = 0 := by
  have hv := (mem_preprocessCandidates A c).mp hc
  exact ⟨fun i => ⟨hv.1 i, c.bounded A hA i⟩, c.primitive A hv, hv.2⟩

theorem cofactorCandidates_length (m N : ℕ) :
    (cofactorCandidates m N).length = ∑ s : Fin (m + 1), N ^ (s.val + 1) * m ^ s.val := by
  simp only [cofactorCandidates, List.length_flatMap, List.length_map, finiteFunctions_length,
    List.map_const', List.sum_replicate, List.finRange, List.map_ofFn, List.sum_ofFn]
  simp

theorem cofactorCandidates_length_le (m N : ℕ) (hN : 1 ≤ N) :
    (cofactorCandidates m N).length ≤ (m + 1) * (N ^ (m + 1) * (m + 1) ^ m) := by
  rw [cofactorCandidates_length]
  calc
    _ ≤ ∑ _s : Fin (m + 1), N ^ (m + 1) * (m + 1) ^ m := by
      apply Finset.sum_le_sum
      intro s _
      apply Nat.mul_le_mul
      · exact Nat.pow_le_pow_right hN (by omega)
      · exact (Nat.pow_le_pow_left (by omega : m ≤ m + 1) s.val).trans
          (Nat.pow_le_pow_right (by omega) (by omega))
    _ = _ := by simp

theorem preprocessCandidates_length_le {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) (hN : 1 ≤ N) :
    (preprocessCandidates A).length ≤ (m + 1) * (N ^ (m + 1) * (m + 1) ^ m) :=
  (List.length_filter_le _ _).trans (cofactorCandidates_length_le m N hN)

/-- The normalized weights are stored once rather than recomputed during queries. -/
structure CompiledCircuit (m N : ℕ) where
  candidate : CofactorCandidate m N
  coefficients : Vector ℕ (candidate.size.val + 1)

def rawCofactorTrace {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (c : CofactorCandidate m N) : Vector (ℤ × ℕ) (c.size.val + 1) :=
  Vector.ofFn fun i => determinantTrace c.size.val
    ((A.submatrix c.support c.columns).submatrix i.succAbove id)

/-- Count the actual determinant arithmetic, Euclidean remainder divisions,
and one absolute-value conversion and normalization quotient per weight. -/
def compileCircuitCounted {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (c : CofactorCandidate m N) : CompiledCircuit m N × ℕ :=
  let traces := rawCofactorTrace A c
  let raw := traces.map fun r => r.1.natAbs
  let divisor := gcdTrace (c.size.val + 1) raw.get
  (⟨c, raw.map fun v => v / divisor.1⟩,
    (∑ i, (traces.get i).2) + divisor.2 + 2 * (c.size.val + 1))

def compileCircuit {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (c : CofactorCandidate m N) : CompiledCircuit m N :=
  (compileCircuitCounted A c).1

namespace CompiledCircuit
variable {m N : ℕ}

def weight (c : CompiledCircuit m N) (i : Fin (c.candidate.size.val + 1)) : ℕ :=
  c.coefficients.get i

def Valid (A : Matrix (Fin N) (Fin m) ℤ) (c : CompiledCircuit m N) : Prop :=
  (∀ i, 0 < c.weight i) ∧
    ∀ j, ∑ i, (c.weight i : ℤ) * A (c.candidate.support i) j = 0

instance (A : Matrix (Fin N) (Fin m) ℤ) (c : CompiledCircuit m N) :
    Decidable (c.Valid A) := inferInstanceAs (Decidable (_ ∧ ∀ _, _))

end CompiledCircuit

@[simp] theorem compileCircuit_weight {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (c : CofactorCandidate m N) (i : Fin (c.size.val + 1)) :
    (compileCircuit A c).weight i = c.weights A i := by
  have he : ((rawCofactorTrace A c).map (fun r => r.1.natAbs)).get =
      (fun i => (cofactorVector (A.submatrix c.support c.columns) i).natAbs) := by
    funext j
    simp [rawCofactorTrace, determinantTrace_value, cofactorVector_natAbs]
  change (((rawCofactorTrace A c).map (fun r => r.1.natAbs)).map
    (fun v => v / (gcdTrace (c.size.val + 1)
      ((rawCofactorTrace A c).map (fun r => r.1.natAbs)).get).1)).get i = _
  rw [Vector.get_map, gcdTrace_value, he]
  rfl

@[simp] theorem compileCircuit_candidate {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (c : CofactorCandidate m N) : (compileCircuit A c).candidate = c := rfl

@[simp] theorem compileCircuit_weights {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (c : CofactorCandidate m N) : (compileCircuit A c).weight = c.weights A :=
  funext (compileCircuit_weight A c)

@[simp] theorem compileCircuit_valid {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (c : CofactorCandidate m N) : (compileCircuit A c).Valid A ↔ c.Valid A := by
  change ((∀ i : Fin (c.size.val + 1), 0 < (compileCircuit A c).weight i) ∧
    ∀ j, ∑ i : Fin (c.size.val + 1), ((compileCircuit A c).weight i : ℤ) *
      A (c.support i) j = 0) ↔ c.Valid A
  simp_rw [compileCircuit_weight]
  rfl

/-- The executable preprocessing output contains actual cached integer weights. -/
def preprocessCircuits {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) :
    List (CompiledCircuit m N) :=
  ((cofactorCandidates m N).map (compileCircuit A)).filter fun c => decide (c.Valid A)

theorem mem_preprocessCircuits {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    {c : CompiledCircuit m N} : c ∈ preprocessCircuits A ↔
      (∃ p : CofactorCandidate m N, compileCircuit A p = c) ∧ c.Valid A := by
  simp [preprocessCircuits, mem_cofactorCandidates]

theorem compile_mem_preprocessCircuits {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (c : CofactorCandidate m N) : compileCircuit A c ∈ preprocessCircuits A ↔ c.Valid A := by
  rw [mem_preprocessCircuits, compileCircuit_valid]
  simp

theorem preprocessCircuits_sound {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) {c : CompiledCircuit m N} (hc : c ∈ preprocessCircuits A) :
    (∀ i, 0 < c.weight i ∧ c.weight i ≤ delta01 m) ∧
    Finset.univ.gcd c.weight = 1 ∧
    ∀ j, ∑ i, (c.weight i : ℤ) * A (c.candidate.support i) j = 0 := by
  obtain ⟨⟨p, rfl⟩, hp⟩ := (mem_preprocessCircuits A).mp hc
  have hs := preprocessCandidates_sound A hA ((mem_preprocessCandidates A p).mpr
    ((compileCircuit_valid A p).mp hp))
  refine ⟨?_, ?_, ?_⟩
  · intro i
    change Fin (p.size.val + 1) at i
    rw [compileCircuit_weight]
    exact hs.1 i
  · rw [compileCircuit_weights]
    exact hs.2.1
  · intro j
    change (∑ i : Fin (p.size.val + 1), ((compileCircuit A p).weight i : ℤ) *
      A (p.support i) j) = 0
    simp_rw [compileCircuit_weight]
    exact hs.2.2 j

theorem preprocessCircuits_length_le {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) (hN : 1 ≤ N) :
    (preprocessCircuits A).length ≤ (m + 1) * (N ^ (m + 1) * (m + 1) ^ m) := by
  apply (List.length_filter_le _ _).trans
  simpa only [List.length_map] using cofactorCandidates_length_le m N hN

/-- Every positive circuit has a positively proportional certificate in the
actual preprocessing output, with the same set of input rows. -/
theorem preprocessCircuits_complete {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A)
    (C : Chain.Threshold.PositiveCircuit (fun i j => (A i j : ℝ))) :
    ∃ c ∈ preprocessCircuits A,
      Set.range c.candidate.support = Set.range C.index ∧
      ∃ scale : ℝ, 0 < scale ∧ ∀ b : Fin N → ℝ,
        (∑ i, (c.weight i : ℝ) * b (c.candidate.support i)) =
          scale * ∑ i, C.mass i * b (C.index i) := by
  obtain ⟨s, hs, e, f, hp, _, hcancel, hrange, scale, hscale, he⟩ :=
    C.exists_cofactor_candidate A hA
  let p : CofactorCandidate m N := ⟨⟨s, by omega⟩, e, f⟩
  have hv : p.Valid A := ⟨fun i => (hp i).1, hcancel⟩
  refine ⟨compileCircuit A p, (compile_mem_preprocessCircuits A p).mpr hv,
    hrange, scale, hscale, ?_⟩
  intro b
  change (∑ i : Fin (s + 1), ((compileCircuit A p).weight i : ℝ) * b (e i)) = _
  simp_rw [compileCircuit_weight]
  exact he b

/-- The parameter-dependent candidate count is singly exponential in a quadratic. -/
theorem cofactorCandidates_length_exp (m N : ℕ) (hN : 1 ≤ N) (hNb : N ≤ 2 ^ (m + 2)) :
    (cofactorCandidates m N).length ≤ 2 ^ (4 * (m + 1) ^ 2) := by
  have hm : m + 1 ≤ 2 ^ (m + 1) := Nat.lt_two_pow_self.le
  calc
    _ ≤ (m + 1) * (N ^ (m + 1) * (m + 1) ^ m) := cofactorCandidates_length_le m N hN
    _ ≤ 2 ^ (m + 1) * ((2 ^ (m + 2)) ^ (m + 1) * (2 ^ (m + 1)) ^ m) := by
      exact Nat.mul_le_mul hm (Nat.mul_le_mul (Nat.pow_le_pow_left hNb _)
        (Nat.pow_le_pow_left hm _))
    _ = 2 ^ ((m + 1) + ((m + 2) * (m + 1) + (m + 1) * m)) := by
      rw [← pow_mul, ← pow_mul, ← pow_add, ← pow_add]
    _ ≤ _ := Nat.pow_le_pow_right (by decide) (by nlinarith)

theorem normal_universe_bound (m : ℕ) : 2 ^ m + m + 1 ≤ 2 ^ (m + 2) := by
  have hm : m < 2 ^ m := Nat.lt_two_pow_self
  rw [show m + 2 = m + 1 + 1 by omega, pow_succ, pow_succ]
  omega

theorem preprocessCircuits_length_exp {m : ℕ}
    (A : Matrix (Fin (2 ^ m + m + 1)) (Fin m) ℤ) :
    (preprocessCircuits A).length ≤ 2 ^ (4 * (m + 1) ^ 2) := by
  apply (List.length_filter_le _ _).trans
  rw [List.length_map]
  exact cofactorCandidates_length_exp m (2 ^ m + m + 1)
    (Nat.succ_le_succ (Nat.zero_le _)) (normal_universe_bound m)

end NetworkSimplex.Threshold
