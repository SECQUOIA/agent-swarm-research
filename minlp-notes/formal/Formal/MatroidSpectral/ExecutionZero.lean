import Formal.MatroidSpectral.ExecutionMarked
import Formal.MatroidSpectral.CoverProducer
import Formal.DAGSpectral.ZeroBitCost

namespace MatroidSpectral.Execution
open DAGSpectral DAGSpectral.NormalizationTrials DAGSpectral.CoverBitCost
open scoped BigOperators

def zeroRun {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (B : ℕ) : List (Finset (Fin m)) × ℕ :=
  let prior := matrixZeroCacheRun (D.atom none)
  let atoms := Vector.ofFn fun e => matrixZeroCacheRun (D.atom (some e))
  let ground := Finset.univ.filter (fun e => (atoms.get e).1 = true)
  let work := traceBitWork B prior.2.1 + prior.2.2 +
    (∑ e : Fin m, (traceBitWork B (atoms.get e).2.1 + (atoms.get e).2.2)) + columnWork m
  if prior.1 then
    let result := profileBasesRun A ground ∅ (fun _ (_ : Fin 0) => 0) 0 B []
    (result.1, work + result.2 + 1)
  else ([], work + 1)

theorem zeroRun_value {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (B : ℕ) :
    (zeroRun A D B).1.toFinset = zeroBasisSet A D := by
  simp only [zeroRun, matrixZeroCacheRun_value, matrixZeroRun_value, Vector.get_ofFn]
  simp only [decide_eq_true_eq]
  split <;> simp_all [profileBasesRun_value, zeroBasisSet, zeroGround]

theorem zeroRun_length {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (B : ℕ) : (zeroRun A D B).1.length ≤ 1 := by
  simp only [zeroRun]
  split
  · rw [profileBasesRun_value]
    simpa using profileBases_length A _ ∅ (fun _ (_ : Fin 0) => 0) 0 []
  · simp

def zeroWorkBound (q p m B : ℕ) : ℕ :=
  (m + 1) * ((2 * p * p) * (256 * (B + 1) ^ 3) + 4 * p * p) + columnWork m +
    profileWorkBound q m 0 0 (markedQueryWork q m 0 0 B) + 1

theorem zeroRun_work {q p m M B : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (hA : MatrixBits A B)
    (hD : ∀ o, MatrixBits (D.atom o) B) :
    (zeroRun A D B).2 ≤ zeroWorkBound q p m B := by
  have hp := matrixZeroRun_bitWork (hD none)
  have hs : (∑ e : Fin m, traceBitWork B (matrixZeroRun (D.atom (some e))).2) ≤
      m * ((2 * p * p) * (256 * (B + 1) ^ 3)) := by
    calc
      _ ≤ ∑ _e : Fin m, ((2 * p * p) * (256 * (B + 1) ^ 3)) :=
        Finset.sum_le_sum (fun e _ => matrixZeroRun_bitWork (hD (some e)))
      _ = _ := by simp
  have hr (ground : Finset (Fin m)) := profileBasesRun_work A ground ∅
    (fun _ (_ : Fin 0) => 0) 0 B [] (by simp) hA (fun _ _ i => Fin.elim0 i)
  simp only [Fintype.card_fin] at hr
  simp only [zeroRun, Vector.get_ofFn, matrixZeroCacheRun_value,
    matrixZeroCacheRun_events, matrixZeroCacheRun_control,
    Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    smul_eq_mul, zeroWorkBound]
  split
  · have hh := hr (Finset.univ.filter (fun e => (matrixZeroRun (D.atom (some e))).1 = true))
    nlinarith
  · nlinarith

end MatroidSpectral.Execution
