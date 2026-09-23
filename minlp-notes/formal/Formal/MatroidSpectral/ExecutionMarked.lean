import Formal.MatroidSpectral.ExecutionProfiles
import Formal.MatroidSpectral.ProfileOracleEvaluation
import Mathlib.Order.WithBot

namespace MatroidSpectral.Execution

instance optionLinearOrder {κ : Type*} [LinearOrder κ] : LinearOrder (Option κ) :=
  inferInstanceAs (LinearOrder (WithBot κ))

def weightCache {m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (w : Fin m → κ → ℕ) : Vector (List (κ × ℕ)) m :=
  Vector.ofFn fun e => (Finset.univ.sort (· ≤ ·)).map (fun i => (i, w e i))

def readWeightCache {m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (cache : Vector (List (κ × ℕ)) m) (e : Fin m) (i : κ) : ℕ :=
  ((cache.get e).lookup i).getD 0

@[simp] theorem readWeightCache_value {m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (w : Fin m → κ → ℕ) : readWeightCache (weightCache w) = w := by
  funext e i
  simp only [readWeightCache, weightCache, Vector.get_ofFn]
  rw [List.lookup_graph _ (by simp)]
  rfl

/-- Restriction, owner marking, and the retained-set intersection use explicit
finite scans. The query itself retains all original representation rows. -/
def markerWork (m d W : ℕ) : ℕ := 8 * (m + 1) ^ 2 * (d + 1) * (W + 1)

def markedQuery {q m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W B : ℕ) (z : κ → Fin (q * W + 1))
    (retained : Finset (Fin m)) : Bool × ℕ :=
  if hf : forced.card ≤ q then
    let cache := weightCache (markedWeight forced (restrictedWeights ground w))
    let query := profileCoefficientQueryRun A
      (readWeightCache cache) (max (q * W) q)
      (max W 1) B (markedCandidate forced hf z) (retained ∩ ground)
    (query.1, query.2 + markerWork m (Fintype.card κ) W)
  else (false, markerWork m (Fintype.card κ) W)

theorem markedQuery_value {q m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W B : ℕ) (z : κ → Fin (q * W + 1))
    (retained : Finset (Fin m)) :
    (markedQuery A ground forced w W B z retained).1 =
      markedProfileOracle A ground forced w W z retained := by
  simp only [markedQuery, readWeightCache_value, markedProfileOracle]
  split <;> simp only [profileCoefficientQueryRun_value]

def markedQueryWork (q m d W B : ℕ) : ℕ :=
  profileCoefficientQueryWork q m (d + 1) (max (q * W) q) (max W 1) B +
    markerWork m d W

theorem markedQuery_work {q m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W B : ℕ)
    (hA : DAGSpectral.MatrixBits A B) (hw : ∀ e ∈ ground, ∀ i, w e i ≤ W)
    (z : κ → Fin (q * W + 1)) (retained : Finset (Fin m)) :
    (markedQuery A ground forced w W B z retained).2 ≤
      markedQueryWork q m (Fintype.card κ) W B := by
  have hweights : ∀ e i, markedWeight forced (restrictedWeights ground w) e i ≤ max W 1 := by
    intro e i
    cases i with
    | none => simp only [markedWeight, Option.elim_none, ownerWeight]; split <;> omega
    | some i => exact (restrictedWeights_le ground w W hw e i).trans (Nat.le_max_left _ _)
  simp only [markedQuery, readWeightCache_value]
  split
  · have hh := profileCoefficientQueryRun_work hA
      (markedWeight forced (restrictedWeights ground w)) hweights (max (q * W) q)
      (markedCandidate forced (by assumption) z) (retained ∩ ground)
    simpa only [Fintype.card_option, markedQueryWork] using
      Nat.add_le_add_right hh (markerWork m (Fintype.card κ) W)
  · exact Nat.le_add_left _ _

def profileBasesRun {q m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W B : ℕ) (coords : List κ) : List (Finset (Fin m)) × ℕ :=
  basesRun ground w W coords (markedQuery A ground forced w W B)

theorem profileBasesRun_value {q m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W B : ℕ) (coords : List κ) :
    (profileBasesRun A ground forced w W B coords).1 =
      profileBases A ground forced w W coords :=
  basesRun_value A ground forced w W coords _ (markedQuery_value A ground forced w W B)

theorem profileBasesRun_work {q m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W B : ℕ) (coords : List κ)
    (hc : coords.length = Fintype.card κ)
    (hA : DAGSpectral.MatrixBits A B) (hw : ∀ e ∈ ground, ∀ i, w e i ≤ W) :
    (profileBasesRun A ground forced w W B coords).2 ≤
      profileWorkBound q m (Fintype.card κ) W
        (markedQueryWork q m (Fintype.card κ) W B) :=
  basesRun_work ground w W coords hc hw _ (markedQuery_work A ground forced w W B hA hw)

end MatroidSpectral.Execution
