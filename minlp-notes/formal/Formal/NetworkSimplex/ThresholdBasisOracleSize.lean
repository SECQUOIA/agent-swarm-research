import Formal.NetworkSimplex.ThresholdBasisOracle
import Formal.NetworkSimplex.ThresholdDeterminant
import Formal.NetworkSimplex.ThresholdDetTrace
import Formal.ReciprocalAnchor.ManyRationalSize
import Formal.ReciprocalAnchor.ManyBitCost

/-! Rational sizes and an explicit preprocessing work ledger for cached basis recovery. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open Matrix ReciprocalAnchor

/-- A signed-subset basis has factorial-bounded determinant and cofactors. -/
theorem unitEntry_det_natAbs {m : ℕ} (A : Matrix (Fin m) (Fin m) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) : A.det.natAbs ≤ m.factorial := by
  simpa only [NetworkSimplex.Threshold.determinantTrace_value] using
    NetworkSimplex.Threshold.determinantTrace_abs m A hA

theorem unitEntry_adjugate_natAbs {m : ℕ} (A : Matrix (Fin m) (Fin m) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) (i j : Fin m) :
    (A.adjugate i j).natAbs ≤ m.factorial := by
  rw [Matrix.adjugate_apply]
  apply unitEntry_det_natAbs
  intro k l
  by_cases hk : k = j
  · subst k
    simp [Matrix.updateRow_apply, Pi.single_apply]
    split_ifs <;> norm_num
  · simpa [Matrix.updateRow_apply, hk] using hA k l

/-- This is O(m log m) bits, and is also bounded by m^2+1 below. -/
def basisEntryBits (m : ℕ) : ℕ := m * m.size + 1

theorem factorial_lt_basisEntryBits (m : ℕ) : m.factorial < 2 ^ basisEntryBits m := by
  have hp := Nat.pow_le_pow_left (Nat.lt_size_self m).le m
  rw [← pow_mul] at hp
  have hpow : 2 ^ (m.size * m) < 2 ^ (m.size * m + 1) :=
    Nat.pow_lt_pow_right (by decide) (by omega)
  simpa only [basisEntryBits, Nat.mul_comm] using
    (Nat.factorial_le_pow m).trans_lt (hp.trans_lt hpow)

theorem basisEntryBits_polynomial (m : ℕ) : basisEntryBits m ≤ m ^ 2 + 1 := by
  have hs : m.size ≤ m := Nat.size_le.mpr m.lt_two_pow_self
  unfold basisEntryBits
  nlinarith

theorem int_factorial_bits {m : ℕ} {z : ℤ} (hz : z.natAbs ≤ m.factorial) :
    RationalBits (z : ℚ) (basisEntryBits m) := by
  have hn := hz.trans_lt (factorial_lt_basisEntryBits m)
  have hd : 1 < 2 ^ basisEntryBits m := Nat.one_lt_two_pow (by unfold basisEntryBits; omega)
  simpa only [RationalBits, Rat.num_intCast, Rat.den_intCast] using And.intro hn hd

/-- The actual adjugate-form inverse has bounded reduced fractions, even for singular bases. -/
theorem inverseRat_integer_bits {m : ℕ} (A : Matrix (Fin m) (Fin m) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) (i j : Fin m) :
    RationalBits (inverseRat (fun r c => (A r c : ℚ)) i j) (basisEntryBits m) := by
  have hdet : Matrix.det (fun r c => (A r c : ℚ)) = (A.det : ℚ) := by
    exact ((Int.castRingHom ℚ).map_det A).symm
  have hadj : Matrix.adjugate (fun r c => (A r c : ℚ)) i j = (A.adjugate i j : ℚ) := by
    exact congrFun (congrFun ((Int.castRingHom ℚ).map_adjugate A).symm i) j
  change RationalBits ((Matrix.det (fun r c => (A r c : ℚ)))⁻¹ *
    Matrix.adjugate (fun r c => (A r c : ℚ)) i j) _
  rw [hdet, hadj, mul_comm, ← div_eq_mul_inv]
  by_cases hd : A.det = 0
  · rw [hd]
    simp only [Int.cast_zero, div_zero]
    exact rationalBits_mono rationalBits_zero (by unfold basisEntryBits; omega)
  · exact rationalBits_fraction hd
      ((unitEntry_adjugate_natAbs A hA i j).trans_lt (factorial_lt_basisEntryBits m))
      ((unitEntry_det_natAbs A hA).trans_lt (factorial_lt_basisEntryBits m))

/-- Every actual cache entry inherits the same width from the integer normal universe. -/
theorem cachedBasis_inverse_bits {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) {C : CachedBasis N m}
    (hC : C ∈ basisLibrary (fun i j => (A i j : ℚ))) (i j : Fin m) :
    RationalBits (C.inverse i j) (basisEntryBits m) := by
  obtain ⟨e, _, rfl⟩ := (mem_basisLibrary_iff _ _).mp hC
  simp only [CachedBasis.inverse, cacheBasis, Vector.get_ofFn]
  have he : Matrix.submatrix (fun i j => (A i j : ℚ)) e id =
      fun r c => ((A.submatrix e id) r c : ℚ) := by ext r c; rfl
  rw [he]
  exact inverseRat_integer_bits (A.submatrix e id) (fun r c => hA (e r) c) i j

/-- Width of a cached-basis candidate, linear in the input right-hand-side width. -/
def basisCandidateBits (m B : ℕ) : ℕ := 1 + m * (basisEntryBits m + B + 1)

/-- Every candidate coordinate partial sum is bounded, including rejected candidates. -/
theorem cachedBasis_candidate_partial_bits {N m B : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) {C : CachedBasis N m}
    (hC : C ∈ basisLibrary (fun i j => (A i j : ℚ))) (table : Fin N → Option ℚ)
    (hB : 0 < B) (hb : ∀ i q, table i = some q → RationalBits q B)
    (i : Fin m) (s : Finset (Fin m)) :
    RationalBits (∑ j ∈ s, C.inverse i j * (table (C.rows j)).getD 0)
      (basisCandidateBits m B) := by
  have hterm (j : Fin m) : RationalBits
      (C.inverse i j * (table (C.rows j)).getD 0) (basisEntryBits m + B) := by
    apply rationalBits_mul (cachedBasis_inverse_bits A hA hC i j)
    cases he : table (C.rows j) with
    | none => exact rationalBits_mono rationalBits_zero hB
    | some q => exact hb _ q he
  apply rationalBits_mono (rationalBits_finset_sum s _ (fun j _ => hterm j))
  unfold basisCandidateBits
  have hc : s.card ≤ m := (Finset.card_le_univ s).trans_eq (Fintype.card_fin m)
  exact Nat.add_le_add_left (Nat.mul_le_mul_right _ hc) 1

theorem cachedBasis_candidate_bits {N m B : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) {C : CachedBasis N m}
    (hC : C ∈ basisLibrary (fun i j => (A i j : ℚ))) (table : Fin N → Option ℚ)
    (hB : 0 < B) (hb : ∀ i q, table i = some q → RationalBits q B) (i : Fin m) :
    RationalBits (C.candidate table i) (basisCandidateBits m B) := by
  simpa only [CachedBasis.candidate, Vector.get_ofFn, Matrix.mulVec, dotProduct] using
    cachedBasis_candidate_partial_bits A hA hC table hB hb i Finset.univ

/-- Integer input normals have one-bit numerator and denominator magnitudes. -/
theorem unitEntry_bits {z : ℤ} (hz : z.natAbs ≤ 1) : RationalBits (z : ℚ) 1 := by
  simp only [RationalBits, Rat.num_intCast, Rat.den_intCast]
  constructor
  · omega
  · norm_num

/-- Validation includes every dot-product partial sum, not only returned candidates. -/
theorem candidate_validation_partial_bits {N m B : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) {C : CachedBasis N m}
    (hC : C ∈ basisLibrary (fun i j => (A i j : ℚ))) (table : Fin N → Option ℚ)
    (hB : 0 < B) (hb : ∀ i q, table i = some q → RationalBits q B)
    (i : Fin N) (s : Finset (Fin m)) :
    RationalBits (∑ j ∈ s, (A i j : ℚ) * C.candidate table j)
      (1 + m * (basisCandidateBits m B + 2)) := by
  have ht (j : Fin m) := rationalBits_mul (unitEntry_bits (hA i j))
    (cachedBasis_candidate_bits A hA hC table hB hb j)
  apply rationalBits_mono (rationalBits_finset_sum s _ (fun j _ => ht j))
  have hc : s.card ≤ m := (Finset.card_le_univ s).trans_eq (Fintype.card_fin m)
  nlinarith [Nat.mul_le_mul_right (1 + basisCandidateBits m B + 1) hc]

/-- An actual successful scan returns a candidate from a cache entry it visited. -/
theorem scanBases_source {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (L : List (CachedBasis N m)) {x : Fin m → ℚ}
    (hx : (scanBases A table L).1 = some x) :
    ∃ C ∈ L, x = C.candidate table := by
  induction L with
  | nil => simp [scanBases] at hx
  | cons C L ih =>
    simp only [scanBases] at hx
    split_ifs at hx with hp hv
    · exact ⟨C, List.mem_cons_self, (Option.some.inj hx).symm⟩
    · obtain ⟨D, hD, he⟩ := ih hx
      exact ⟨D, List.mem_cons_of_mem _ hD, he⟩
    · obtain ⟨D, hD, he⟩ := ih hx
      exact ⟨D, List.mem_cons_of_mem _ hD, he⟩

/-- The returned profile inherits the candidate bound without an extra width hypothesis. -/
theorem recoverFromCache_bits {N m B : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) (table : Fin N → Option ℚ)
    (hB : 0 < B) (hb : ∀ i q, table i = some q → RationalBits q B)
    {x : Fin m → ℚ}
    (hx : recoverFromCache (fun i j => (A i j : ℚ)) table
      (basisLibrary (fun i j => (A i j : ℚ))) = some x) (i : Fin m) :
    RationalBits (x i) (basisCandidateBits m B) := by
  obtain ⟨C, hC, rfl⟩ := scanBases_source _ _ _ hx
  exact cachedBasis_candidate_bits A hA hC table hB hb i

/-- A multiply-accumulate costs two primitive rational operations. Doubling
the scan ledger therefore bounds the same execution in the unfused model. -/
theorem scanBases_primitive_charge_le {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (L : List (CachedBasis N m)) :
    2 * (scanBases A table L).2 ≤ L.length * (2 * basisTrialCharge N m) := by
  have h := Nat.mul_le_mul_left 2 (scanBases_charge_le A table L)
  nlinarith

end NetworkSimplex.Chain.Threshold
