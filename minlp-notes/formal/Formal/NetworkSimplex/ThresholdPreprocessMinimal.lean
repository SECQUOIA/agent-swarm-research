import Formal.NetworkSimplex.ThresholdCircuitPreprocess

/-! The executable cofactor filter outputs genuine minimally dependent positive circuits. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators
open Chain.Threshold

/-- Positivity of a normalized cofactor forces the corresponding deleted minor
nonzero. In particular, accepted candidates have an invertible tail minor. -/
theorem CofactorCandidate.tail_minor_ne_zero {m N : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N) (hc : c.Valid A) :
    ((A.submatrix c.support c.columns).submatrix Fin.succ id).det ≠ 0 := by
  have hraw : 0 < (cofactorVector (A.submatrix c.support c.columns) 0).natAbs :=
    (hc.1 0).trans_le (primitiveWeights_le _ 0)
  rw [cofactorVector_natAbs] at hraw
  simpa only [Fin.succAbove_zero] using Int.natAbs_pos.mp hraw

/-- Every accepted candidate is affinely independent on its full original rows. -/
theorem CofactorCandidate.affineIndependent {m N : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N) (hc : c.Valid A) :
    AffineIndependent ℝ (fun i => fun j => (A (c.support i) j : ℝ)) := by
  classical
  let B : Matrix (Fin (c.size.val + 1)) (Fin c.size.val) ℝ :=
    fun i j => A (c.support i) (c.columns j)
  have hminor : (B.submatrix Fin.succ id).det ≠ 0 := by
    have hmap := RingHom.map_det (Int.castRingHom ℝ)
      ((A.submatrix c.support c.columns).submatrix Fin.succ id)
    intro hz
    have hcast : ((((A.submatrix c.support c.columns).submatrix Fin.succ id).det : ℤ) : ℝ) = 0 :=
      hmap.trans hz
    exact c.tail_minor_ne_zero A hc (by exact_mod_cast hcast)
  have hli : LinearIndependent ℝ (fun i : Fin c.size.val => B i.succ) :=
    Matrix.linearIndependent_rows_of_det_ne_zero hminor
  let w : Fin (c.size.val + 1) → ℝ := fun i => c.weights A i
  have hw : ∀ i, 0 < w i := fun i => by dsimp [w]; exact_mod_cast hc.1 i
  have hsum : 0 < ∑ i, w i :=
    Finset.sum_pos' (fun i _ => (hw i).le) ⟨0, Finset.mem_univ _, hw 0⟩
  have hwc : ∑ i, w i • B i = 0 := by
    ext j
    have h := hc.2 (c.columns j)
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply]
    dsimp [w, B]
    exact_mod_cast h
  apply (affineIndependent_iff_of_fintype ℝ _).mpr
  intro v hv0 hvc i
  rw [Finset.weightedVSub_eq_linear_combination _ hv0] at hvc
  have hvB : ∑ i, v i • B i = 0 := by
    ext j
    have h := congrFun hvc (c.columns j)
    simpa only [B, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] using h
  have hprop := relation_eq_of_tail_independent B hli w v (ne_of_gt (hw 0)) hwc hvB
  have hs : (∑ i, v i) = (v 0 / w 0) * ∑ i, w i := by
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl (fun i _ => hprop i)
  rw [hv0] at hs
  have hz : v 0 / w 0 = 0 := (mul_eq_zero.mp hs.symm).resolve_right (ne_of_gt hsum)
  simpa only [hz, zero_mul] using hprop i

/-- The executable filter cannot accept repeated input-row indices. -/
theorem CofactorCandidate.support_injective {m N : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N) (hc : c.Valid A) :
    Function.Injective c.support := by
  intro i j hij
  apply (c.affineIndependent A hc).injective
  change (fun k => (A (c.support i) k : ℝ)) = (fun k => (A (c.support j) k : ℝ))
  simp only [hij]

/-- The normalized real circuit directly represented by an accepted candidate. -/
noncomputable def CofactorCandidate.positiveCircuit {m N : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N) (hc : c.Valid A) :
    PositiveCircuit (fun i j => (A i j : ℝ)) := by
  let w : Fin (c.size.val + 1) → ℝ := fun i => c.weights A i
  have hw : ∀ i, 0 < w i := fun i => by dsimp [w]; exact_mod_cast hc.1 i
  have hs : 0 < ∑ i, w i :=
    Finset.sum_pos' (fun i _ => (hw i).le) ⟨0, Finset.mem_univ _, hw 0⟩
  exact {
    size := c.size.val + 1
    index := ⟨c.support, c.support_injective A hc⟩
    mass := fun i => w i / (∑ j, w j)
    positive := fun i => div_pos (hw i) hs
    total := by rw [← Finset.sum_div, div_self (ne_of_gt hs)]
    cancel := by
      ext j
      have h : ∑ i, w i * (A (c.support i) j : ℝ) = 0 := by
        dsimp [w]
        exact_mod_cast hc.2 j
      simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply]
      simp_rw [div_mul_eq_mul_div, ← Finset.sum_div]
      change (∑ i, w i * (A (c.support i) j : ℝ)) / (∑ i, w i) = 0
      rw [h, zero_div]
    independent := c.affineIndependent A hc
  }

/-- The constructed circuit uses exactly the candidate's input rows. -/
theorem CofactorCandidate.positiveCircuit_range {m N : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N) (hc : c.Valid A) :
    Set.range (c.positiveCircuit A hc).index = Set.range c.support := rfl

/-- Normalization preserves every objective exactly after division by the total weight. -/
theorem CofactorCandidate.positiveCircuit_objective {m N : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) (c : CofactorCandidate m N) (hc : c.Valid A)
    (b : Fin N → ℝ) :
    (∑ i, (c.positiveCircuit A hc).mass i * b ((c.positiveCircuit A hc).index i)) =
      (∑ i, (c.weights A i : ℝ) * b (c.support i)) / ∑ i, (c.weights A i : ℝ) := by
  change (∑ i, (c.weights A i : ℝ) / (∑ j, (c.weights A j : ℝ)) * b (c.support i)) = _
  simp only [div_mul_eq_mul_div, Finset.sum_div]

/-- Every entry of the actual compiled preprocessing output represents a genuine
positive circuit, with exactly its support and normalized integer weights. -/
theorem preprocessCircuits_are_positiveCircuits {m N : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) {c : CompiledCircuit m N}
    (hc : c ∈ preprocessCircuits A) :
    Function.Injective c.candidate.support ∧
    ∃ C : PositiveCircuit (fun i j => (A i j : ℝ)),
      Set.range C.index = Set.range c.candidate.support ∧
      ∀ b : Fin N → ℝ,
        (∑ i, C.mass i * b (C.index i)) =
          (∑ i, (c.weight i : ℝ) * b (c.candidate.support i)) / ∑ i, (c.weight i : ℝ) := by
  obtain ⟨⟨p, rfl⟩, hp⟩ := (mem_preprocessCircuits A).mp hc
  have hv := (compileCircuit_valid A p).mp hp
  refine ⟨p.support_injective A hv, p.positiveCircuit A hv, p.positiveCircuit_range A hv, ?_⟩
  intro b
  change (∑ i, (p.positiveCircuit A hv).mass i * b ((p.positiveCircuit A hv).index i)) =
    (∑ i : Fin (p.size.val + 1), ((compileCircuit A p).weight i : ℝ) * b (p.support i)) /
      ∑ i : Fin (p.size.val + 1), ((compileCircuit A p).weight i : ℝ)
  simp_rw [compileCircuit_weight]
  exact p.positiveCircuit_objective A hv b

end NetworkSimplex.Threshold
