import Formal.NetworkSimplex.ThresholdUnreducedLift
import Formal.NetworkSimplex.ThresholdSignedUniverse
import Formal.NetworkSimplex.ThresholdRowOccurrences
import Formal.NetworkSimplex.ThresholdBranchValidity

/-! Actual full-profile source rows, their signed-subset encoding, and original
flow/product coefficient bounds before residual elimination. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold
variable {m : ℕ} {I : Type*}

/-- The original d=m+1 states are the row coordinates. The auxiliary zero-capacity
state in `unreducedData` is bookkeeping for reuse of the existing row syntax. -/
abbrev UnreducedRow (m : ℕ) (I : Type*) := ProfileRow (m + 1) I

def signedProfileNormal {d : ℕ} : ProfileNormal d → Fin (2 ^ (d + 1))
  | .subset s => signedPack false s
  | .negativeSingleton j => signedPack true {j}
  | .negativeTotal => signedPack true Finset.univ

theorem signedProfileNormal_value {d : ℕ} (p : ProfileNormal d) (w : Fin d → ℝ) :
    (∑ j, (signedKeyNormal (signedProfileNormal p) j : ℝ) * w j) = p.value w := by
  cases p with
  | subset s => simp [signedProfileNormal, signedKeyNormal_pack, signedSubsetVector,
      ProfileNormal.value, Finset.sum_ite_mem]
  | negativeSingleton j => simp [signedProfileNormal, signedKeyNormal_pack,
      signedSubsetVector, ProfileNormal.value]
  | negativeTotal => simp [signedProfileNormal, signedKeyNormal_pack,
      signedSubsetVector, ProfileNormal.value, Finset.sum_neg_distrib]

/-- The upper endpoint is kept in its literal full-profile form -w(B∪N)≤-R. -/
def unreducedKey (D : ReductionData m I) : UnreducedRow m I → Fin (2 ^ (m + 1 + 1))
  | .endpointA i => signedPack true (Finset.univ.filter (fun j => ¬observesA (D.c i j)))
  | r => signedProfileNormal ((unreducedData D).rowNormal r)

def unreducedExpression (D : ReductionData m I) :
    UnreducedRow m I → AffineExpression (Coordinate (m + 1) I)
  | .endpointA i => .neg (residualExpression (unreducedData D) i)
  | r => rowExpression (unreducedData D) r

def unreducedRhs (D : ReductionData m I) : UnreducedRow m I → ℝ
  | .endpointA i => -residual (D.c i) (D.u i) (D.v i) (D.xa i)
  | r => (unreducedData D).rowRhs r

def UnreducedRows (D : ReductionData m I) (w : Fin (m + 1) → ℝ) : Prop :=
  ∀ r, ∑ j, (signedKeyNormal (unreducedKey D r) j : ℝ) * w j ≤ unreducedRhs D r

private theorem unreduced_residual (D : ReductionData m I) (i : I) :
    residual ((unreducedData D).c i) ((unreducedData D).u i)
      ((unreducedData D).v i) ((unreducedData D).xa i) =
      residual (D.c i) (D.u i) (D.v i) (D.xa i) := by
  simp [unreducedData, residual, Fin.sum_univ_succ, observesA]

/-- The expression is in original flow/product coordinates, before eliminating any
original state. The added bookkeeping state's capacity is fixed to zero. -/
theorem unreducedExpression_eval (D : ReductionData m I) (xb : I → ℝ)
    (r : UnreducedRow m I) :
    (unreducedExpression D r).eval (coordinates (unreducedData D) xb) = unreducedRhs D r := by
  cases r <;> simp only [unreducedExpression, unreducedRhs]
  all_goals first
    | exact rowExpression_eval (unreducedData D) xb (fun _ => rfl) _
    | simp [AffineExpression.eval, residualExpression_eval (unreducedData D) xb _ rfl,
        unreduced_residual]

private theorem unreduced_endpoint_iff (D : ReductionData m I) (w : Fin (m + 1) → ℝ)
    (hs : ∑ j, w j = D.total) (i : I) :
    (∑ j, (signedKeyNormal (unreducedKey D (.endpointA i)) j : ℝ) * w j ≤
        unreducedRhs D (.endpointA i)) ↔
      ((unreducedData D).rowNormal (.endpointA i)).value w ≤
        (unreducedData D).rowRhs (.endpointA i) := by
  have hpartition : (∑ j, if observesA (D.c i j) then w j else 0) +
      (∑ j, if ¬observesA (D.c i j) then w j else 0) = ∑ j, w j := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j _
    split_ifs <;> simp_all
  have hneg : (∑ j, (signedKeyNormal (unreducedKey D (.endpointA i)) j : ℝ) * w j) =
      -(∑ j, if ¬observesA (D.c i j) then w j else 0) := by
    simp [unreducedKey, signedKeyNormal_pack, signedSubsetVector,
      ← Finset.sum_neg_distrib, ite_mul, apply_ite]
  rw [hneg]
  simp only [unreducedRhs, ReductionData.rowNormal, ReductionData.rowRhs,
    ProfileNormal.value, Finset.sum_filter, unreduced_residual]
  change _ ↔ (∑ j, if observesA (D.c i j) then w j else 0) ≤ D.total - _
  constructor <;> intro h <;> linarith

/-- The full original profile is exactly the finite signed-subset source-row system. -/
theorem unreducedRows_iff_fullProfile (D : ReductionData m I) (w : Fin (m + 1) → ℝ) :
    UnreducedRows D w ↔ D.FullProfile w := by
  rw [← unreducedData_reduced_iff, ← ReductionData.rows_iff_reducedProfile]
  constructor
  · intro h
    have hl := h .totalLower
    have hu := h .totalUpper
    simp only [unreducedKey, signedProfileNormal_value, unreducedRhs,
      ReductionData.rowNormal, ReductionData.rowRhs, ProfileNormal.value] at hl hu
    have hs : ∑ j, w j = D.total := by
      change -(∑ j, w j) ≤ 0 - D.total at hl
      change (∑ j, w j) ≤ D.total at hu
      linarith
    intro r
    have hh := h r
    cases r
    case endpointA i => exact (unreduced_endpoint_iff D w hs i).mp hh
    all_goals simpa only [unreducedKey, signedProfileNormal_value, unreducedRhs] using hh
  · intro h
    have hr := ((unreducedData D).rows_iff_reducedProfile w).mp h
    have hs : ∑ j, w j = D.total := by
      have hl := hr.2.2.1
      have hu := hr.2.1
      change -(∑ j, w j) ≤ 0 - D.total at hl
      change (∑ j, w j) ≤ D.total at hu
      linarith
    intro r
    have hh := h r
    cases r
    case endpointA i => exact (unreduced_endpoint_iff D w hs i).mpr hh
    all_goals simpa only [unreducedKey, signedProfileNormal_value, unreducedRhs] using hh

/-- Every literal full-profile source normal is in the signed-subset universe,
with zero rows explicitly retained for their scalar checks. -/
theorem unreduced_normal_mem_or_zero (D : ReductionData m I) (r : UnreducedRow m I) :
    signedKeyNormal (unreducedKey D r) ∈ signedSubsetUniverse (m + 1) ∨
      signedKeyNormal (unreducedKey D r) = 0 := signedKeyNormal_mem_or_zero _

/-- No source row has a flow or product coefficient outside {-1,0,1}. -/
theorem unreduced_coefficient_unit [DecidableEq I] (D : ReductionData m I)
    (r : UnreducedRow m I) (z : Coordinate (m + 1) I) (hz : FlowOrProduct z) :
    ((unreducedExpression D r).coefficient z).natAbs ≤ 1 := by
  have hr := row_flow_product_unit (unreducedData D) r z hz
  change -1 ≤ (rowExpression (unreducedData D) r).coefficient z ∧
    (rowExpression (unreducedData D) r).coefficient z ≤ 1 at hr
  cases r <;> simp only [unreducedExpression]
  all_goals try omega
  rename_i i
  have hb := row_flow_product_unit (unreducedData D) (.endpointB i) z hz
  change -1 ≤ (residualExpression (unreducedData D) i).coefficient z ∧
    (residualExpression (unreducedData D) i).coefficient z ≤ 1 at hb
  simp only [AffineExpression.coefficient, Int.natAbs_neg]
  omega

/-- The unreduced ambient coefficient bound now applies to actual original rows,
with no caller-supplied unit-coefficient hypothesis. -/
theorem unreduced_compiled_coefficient_bound [DecidableEq I] (D : ReductionData m I)
    (c : CompiledCircuit (m + 1) (2 ^ (m + 1 + 1)))
    (hc : c ∈ preprocessCircuits (signedKeyNormal (d := m + 1)))
    (rows : Fin (c.candidate.size.val + 1) → UnreducedRow m I)
    (z : Coordinate (m + 1) I) (hz : FlowOrProduct z) :
    (∑ i, (c.weight i : ℤ) * (unreducedExpression D (rows i)).coefficient z).natAbs ≤
      (m + 1 + 1) * delta01 (m + 1) := by
  apply signed_compiled_coefficient_bound c hc
  intro i
  exact unreduced_coefficient_unit D (rows i) z hz

/-- Every actual full-profile row has a signed zero-one normal. -/
theorem unreduced_rows_signed (D : ReductionData m I) :
    RowSignedZeroOne (fun r : UnreducedRow m I => signedKeyNormal (unreducedKey D r)) :=
  fun r => signedKeyNormal_signed (m + 1) (unreducedKey D r)

/-- Exact full-profile feasibility is decided by bounded integer certificates of
actual source rows, including zero-normal scalar checks. -/
theorem fullProfile_iff_unreduced_tests [Finite I] (D : ReductionData m I) :
    (∃ w, D.FullProfile w) ↔
      ∀ s : ℕ, s ≤ m + 1 + 1 → ∀ e : Fin s ↪ UnreducedRow m I, ∀ p : Fin s → ℕ,
        (∀ i, 0 < p i ∧ p i ≤ delta01 (m + 1)) → Finset.univ.gcd p = 1 →
        (∀ j, ∑ i, (p i : ℤ) * signedKeyNormal (unreducedKey D (e i)) j = 0) →
        0 ≤ ∑ i, (p i : ℝ) * unreducedRhs D (e i) := by
  let : Fintype I := Fintype.ofFinite I
  have he := feasible_iff_bounded_integer_tests
    (fun r : UnreducedRow m I => signedKeyNormal (unreducedKey D r))
    (unreduced_rows_signed D) (unreducedRhs D)
  apply Iff.trans ?_ he
  exact exists_congr fun w => (unreducedRows_iff_fullProfile D w).symm

/-- Expanding a compiled signed-universe circuit through matching actual source
rows gives a valid original-coordinate inequality at every feasible full profile. -/
theorem unreduced_compiled_branch_valid (D : ReductionData m I)
    (c : CompiledCircuit (m + 1) (2 ^ (m + 1 + 1)))
    (hc : c ∈ preprocessCircuits (signedKeyNormal (d := m + 1)))
    (rows : Fin (c.candidate.size.val + 1) → UnreducedRow m I)
    (hr : ∀ i, unreducedKey D (rows i) = c.candidate.support i)
    (w : Fin (m + 1) → ℝ) (hw : D.FullProfile w) :
    0 ≤ ∑ i, (c.weight i : ℝ) * unreducedRhs D (rows i) := by
  have hrows := (unreducedRows_iff_fullProfile D w).mpr hw
  apply integer_cancel_valid
    (fun i j => signedKeyNormal (c.candidate.support i) j)
    (fun i => unreducedRhs D (rows i)) id c.weight
    (preprocessCircuits_sound _ (signedKeyNormal_signed (m + 1)) hc).2.2 (x := w)
  intro i
  simpa only [hr i] using hrows (rows i)

end NetworkSimplex.Chain.Threshold
