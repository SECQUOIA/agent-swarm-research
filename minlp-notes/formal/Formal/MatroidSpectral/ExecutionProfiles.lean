import Formal.MatroidSpectral.ExecutionCollection
import Formal.MatroidSpectral.ProfileProducerBases

namespace MatroidSpectral.Execution
open scoped BigOperators

/-- Operand-dependent digit charges for ordinary profile comparisons. The
restriction agrees with the original labels on every returned base. -/
def profileComparisonWork {m : ℕ} {κ : Type*} [Fintype κ]
    (ground : Finset (Fin m)) (w : Fin m → κ → ℕ)
    (B C : Finset (Fin m)) : ℕ :=
  DAGSpectral.ExplicitDAG.keyBitWork ∅
    (fun e i => (restrictedWeights ground w e i : ℤ))
    (B.sort (· ≤ ·)) (C.sort (· ≤ ·))

def profileComparisonBound (m d W : ℕ) : ℕ :=
  DAGSpectral.ExplicitDAG.keyWorkBound m m d 0 (W + 1)

theorem profileComparisonWork_le {m : ℕ} {κ : Type*} [Fintype κ]
    (ground : Finset (Fin m)) (w : Fin m → κ → ℕ) (W : ℕ)
    (hw : ∀ e ∈ ground, ∀ i, w e i ≤ W) (B C : Finset (Fin m)) :
    profileComparisonWork ground w B C ≤ profileComparisonBound m (Fintype.card κ) W := by
  apply DAGSpectral.ExplicitDAG.keyBitWork_le
  · intro e i
    change restrictedWeights ground w e i < 2 ^ (W + 1)
    exact (restrictedWeights_le ground w W hw e i).trans_lt
      ((Nat.lt_two_pow_self (n := W)).trans_le
        (Nat.pow_le_pow_right (by decide) (by omega)))
  · simpa using Finset.card_le_univ B
  · simpa using Finset.card_le_univ C

/-- This is the outer implementation of the represented-profile producer. The
query parameter is instantiated by the determinant/interpolation bit runner;
the equality hypothesis below is not an assumed mathematical support oracle. -/
def basesRun {q m : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (ground : Finset (Fin m)) (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ)
    (query : (κ → Fin (q * W + 1)) → Finset (Fin m) → Bool × ℕ) :
    List (Finset (Fin m)) × ℕ :=
  let raw := coordinateRun q (q * W) coords query ground
  let chosen := deduplicate (naturalProfile w) (profileComparisonWork ground w)
    (columnWork m) raw.1
  (chosen.1, raw.2 + chosen.2)

/-- The restricted operands used for the comparison charge are exactly the
original key operands on every object that reaches deduplication. This does not
assume a support-oracle specification. -/
theorem basesRun_comparison_labels {q m : ℕ} {κ : Type*} [DecidableEq κ]
    (ground : Finset (Fin m)) (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ)
    (query : (κ → Fin (q * W + 1)) → Finset (Fin m) → Bool × ℕ)
    {B : Finset (Fin m)} (hB : B ∈ (coordinateRun q (q * W) coords query ground).1) :
    (∀ e ∈ B, restrictedWeights ground w e = w e) ∧
      naturalProfile (restrictedWeights ground w) B = naturalProfile w B := by
  have hs : B ⊆ ground := candidates_subset q query ground _ hB
  exact ⟨fun e he => by funext i; exact if_pos (hs he),
    restrictedWeights_profile ground B w hs⟩

theorem basesRun_value {q m : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ)
    (query : (κ → Fin (q * W + 1)) → Finset (Fin m) → Bool × ℕ)
    (hquery : ∀ z S, (query z S).1 = markedProfileOracle A ground forced w W z S) :
    (basesRun ground w W coords query).1 = profileBases A ground forced w W coords := by
  have heq : (fun z S => (query z S).1) = markedProfileOracle A ground forced w W :=
    funext (fun z => funext (hquery z))
  simp only [basesRun, deduplicate_value, coordinateRun_value, heq, profileBases]

def profileWorkBound (q m d W Q : ℕ) : ℕ :=
  let R := (q * W + 1) ^ d
  R * ((m + 1) * Q + (m + 2) * columnWork m + (d + 1) * (q * W + 1)) +
    R ^ 2 * profileComparisonBound m d W + R * (columnWork m + 1)

theorem basesRun_work {q m Q : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (ground : Finset (Fin m)) (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ)
    (hc : coords.length = Fintype.card κ)
    (hw : ∀ e ∈ ground, ∀ i, w e i ≤ W)
    (query : (κ → Fin (q * W + 1)) → Finset (Fin m) → Bool × ℕ)
    (hq : ∀ z S, (query z S).2 ≤ Q) :
    (basesRun ground w W coords query).2 ≤
      profileWorkBound q m (Fintype.card κ) W Q := by
  have hr := coordinateRun_work q (q * W) coords query hq ground
  have hl := coordinateRun_length q (q * W) coords query ground
  have hd := deduplicate_work (naturalProfile w) (profileComparisonWork ground w)
    (columnWork m) (coordinateRun q (q * W) coords query ground).1
    (fun B _ C _ => profileComparisonWork_le ground w W hw B C)
  rw [hc] at hr hl
  have hd' : (deduplicate (naturalProfile w) (profileComparisonWork ground w)
      (columnWork m) (coordinateRun q (q * W) coords query ground).1).2 ≤
      ((q * W + 1) ^ Fintype.card κ) ^ 2 * profileComparisonBound m (Fintype.card κ) W +
        (q * W + 1) ^ Fintype.card κ * (columnWork m + 1) := by
    apply hd.trans
    gcongr
  exact (Nat.add_le_add hr hd').trans_eq (by dsimp [profileWorkBound]; omega)

end MatroidSpectral.Execution
