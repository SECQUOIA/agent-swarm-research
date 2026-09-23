import Formal.NetworkSimplex.ThresholdCofactors
import Formal.NetworkSimplex.ThresholdMinor
import Formal.NetworkSimplex.ThresholdDeterminant

/-! Positive primitive integer circuit weights with the zero-one determinant bound. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators

/-- A uniquely determined positive relation makes every proper row deletion independent. -/
theorem tail_independent_of_kernel_unique {s m : ℕ}
    (A : Matrix (Fin (s + 1)) (Fin m) ℝ) (w : Fin (s + 1) → ℝ)
    (hw : 0 < w 0)
    (hu : ∀ v : Fin (s + 1) → ℝ, (∑ i, v i • A i) = 0 →
      ∀ i, v i = (∑ j, v j) * w i) :
    LinearIndependent ℝ (fun i : Fin s => A i.succ) := by
  rw [Fintype.linearIndependent_iff]
  intro v hv i
  let v' : Fin (s + 1) → ℝ := Fin.cons 0 v
  have hc : (∑ j, v' j • A j) = 0 := by simpa [v', Fin.sum_univ_succ] using hv
  have hz := hu v' hc 0
  have hsum : (∑ j, v' j) = 0 := by
    have he : (∑ j, v' j) * w 0 = 0 := by simpa [v'] using hz.symm
    exact (mul_eq_zero.mp he).resolve_right (ne_of_gt hw)
  have hi := hu v' hc i.succ
  simpa [v', hsum] using hi

/-- An invertible tail minor makes the first entry determine an entire relation. -/
theorem relation_eq_of_tail_independent {s k : ℕ}
    (A : Matrix (Fin (s + 1)) (Fin k) ℝ)
    (hA : LinearIndependent ℝ (fun i : Fin s => A i.succ))
    (w v : Fin (s + 1) → ℝ) (hw0 : w 0 ≠ 0)
    (hw : ∑ i, w i • A i = 0) (hv : ∑ i, v i • A i = 0) :
    ∀ i, v i = (v 0 / w 0) * w i := by
  let u := fun i => v i - (v 0 / w 0) * w i
  have hu0 : u 0 = 0 := by dsimp [u]; field_simp; ring
  have huc : ∑ i, u i • A i = 0 := by
    simp only [u, sub_smul, mul_smul, Finset.sum_sub_distrib,
      ← Finset.smul_sum, hv, hw, smul_zero, sub_self]
  have hut : ∑ i : Fin s, u i.succ • A i.succ = 0 := by
    simpa [Fin.sum_univ_succ, hu0] using huc
  have hz := Fintype.linearIndependent_iff.mp hA (fun i => u i.succ) hut
  intro i
  apply sub_eq_zero.mp
  change u i = 0
  exact Fin.cases hu0 hz i

/-- Every positive minimally dependent row-signed zero-one family has primitive
positive integer weights bounded by the largest zero-one minor. -/
theorem exists_primitive_bounded_cofactor_weights {s m : ℕ}
    (A : Matrix (Fin (s + 1)) (Fin m) ℤ) (hA : RowSignedZeroOne A)
    (w : Fin (s + 1) → ℝ) (hw : ∀ i, 0 < w i)
    (hc : ∑ i, w i • (fun j => (A i j : ℝ)) = 0)
    (hli : LinearIndependent ℝ (fun i : Fin s => fun j => (A i.succ j : ℝ))) :
    ∃ e : Fin s ↪ Fin m, ∃ p : Fin (s + 1) → ℕ,
      p = primitiveWeights (fun i => (cofactorVector (A.submatrix id e) i).natAbs) ∧
      (∀ i, 0 < p i ∧ p i ≤ delta01 m) ∧ Finset.univ.gcd p = 1 ∧
      ∀ j, ∑ i, (p i : ℤ) * A i j = 0 := by
  classical
  let T : Matrix (Fin s) (Fin m) ℝ := fun i j => A i.succ j
  obtain ⟨e, he⟩ := exists_nonsingular_coordinate_minor T hli
  have hsm : s ≤ m := independent_rows_le_columns T hli
  let B : Matrix (Fin (s + 1)) (Fin s) ℤ := A.submatrix id e
  have hminor : (B.submatrix Fin.succ id).det ≠ 0 := by
    intro hz
    apply he
    have hmap := RingHom.map_det (Int.castRingHom ℝ) (B.submatrix Fin.succ id)
    rw [hz, map_zero] at hmap
    exact hmap.symm
  let c := cofactorVector B
  have hc0 : c 0 ≠ 0 := by
    apply cofactorVector_ne_zero
    simpa using hminor
  let BR : Matrix (Fin (s + 1)) (Fin s) ℝ := fun i j => B i j
  have hBR : LinearIndependent ℝ (fun i : Fin s => BR i.succ) := by
    exact Matrix.linearIndependent_rows_of_det_ne_zero he
  have hwB : ∑ i, w i • BR i = 0 := by
    ext j
    have h := congrFun hc (e j)
    simpa [BR, B, Matrix.submatrix, Finset.sum_apply] using h
  have hcB : ∑ i, (c i : ℝ) • BR i = 0 := by
    ext j
    have h := cofactorVector_cancels B j
    have h' : (∑ i, (c i : ℝ) * (B i j : ℝ)) = 0 := by exact_mod_cast h
    simpa [BR, Finset.sum_apply] using h'
  have hprop := relation_eq_of_tail_independent BR hBR w (fun i => (c i : ℝ))
    (ne_of_gt (hw 0)) hwB hcB
  let scale : ℝ := (c 0 : ℝ) / w 0
  have hscale : scale ≠ 0 := div_ne_zero (by exact_mod_cast hc0) (ne_of_gt (hw 0))
  let v : Fin (s + 1) → ℕ := fun i => (c i).natAbs
  have hvcast (i : Fin (s + 1)) : (v i : ℝ) = |scale| * w i := by
    have hn : (v i : ℝ) = |(c i : ℝ)| := by
      simp only [v, Nat.cast_natAbs, Int.cast_abs]
    rw [hn, hprop i, abs_mul, abs_of_pos (hw i)]
  have hvpos : ∀ i, 0 < v i := by
    intro i
    have h : (0 : ℝ) < (v i : ℝ) := by
      rw [hvcast]
      exact mul_pos (abs_pos.mpr hscale) (hw i)
    exact_mod_cast h
  have hvc : ∀ j, ∑ i, (v i : ℤ) * A i j = 0 := by
    intro j
    have h : ∑ i, (v i : ℝ) * (A i j : ℝ) = 0 := by
      simp_rw [hvcast, mul_assoc, ← Finset.mul_sum]
      have hcj := congrFun hc j
      simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] at hcj
      rw [hcj, mul_zero]
    exact_mod_cast h
  have hvne : ∃ i, v i ≠ 0 := ⟨0, ne_of_gt (hvpos 0)⟩
  refine ⟨e, primitiveWeights v, rfl, ?_, primitiveWeights_gcd v hvne,
    primitiveWeights_cancels v A hvne hvc⟩
  intro i
  refine ⟨primitiveWeights_pos v i (hvpos i), (primitiveWeights_le v i).trans ?_⟩
  change (cofactorVector B i).natAbs ≤ delta01 m
  rw [cofactorVector_natAbs]
  exact ((hA.submatrix id e).submatrix i.succAbove id).det_natAbs_le hsm

/-- The bounded primitive representative, without retaining its selected columns. -/
theorem exists_primitive_bounded_weights {s m : ℕ}
    (A : Matrix (Fin (s + 1)) (Fin m) ℤ) (hA : RowSignedZeroOne A)
    (w : Fin (s + 1) → ℝ) (hw : ∀ i, 0 < w i)
    (hc : ∑ i, w i • (fun j => (A i j : ℝ)) = 0)
    (hli : LinearIndependent ℝ (fun i : Fin s => fun j => (A i.succ j : ℝ))) :
    ∃ p : Fin (s + 1) → ℕ,
      (∀ i, 0 < p i ∧ p i ≤ delta01 m) ∧ Finset.univ.gcd p = 1 ∧
      ∀ j, ∑ i, (p i : ℤ) * A i j = 0 := by
  obtain ⟨_, p, _, hp, hg, hc⟩ :=
    exists_primitive_bounded_cofactor_weights A hA w hw hc hli
  exact ⟨p, hp, hg, hc⟩

end NetworkSimplex.Threshold
