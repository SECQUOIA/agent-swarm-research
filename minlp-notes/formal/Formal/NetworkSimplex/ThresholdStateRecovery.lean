import Formal.NetworkSimplex.ThresholdGreedy
import Formal.NetworkSimplex.ProfileHull

/-! Executable rational greedy recovery of every gadget's state flows. -/
namespace NetworkSimplex.Chain
open scoped BigOperators

variable {L N : ℕ}

def rationalFixedA (c : Fin N → StateClass) (u v w : Fin N → ℚ) (j : Fin N) : ℚ :=
  match c j with
  | .aOnly | .both => u j
  | .bOnly => w j - v j
  | .neither => 0

def rationalFreeA (c : Fin N → StateClass) (w : Fin N → ℚ) (j : Fin N) : ℚ :=
  if c j = .neither then w j else 0

@[simp] theorem rationalFixedA_cast (c : Fin N → StateClass) (u v w : Fin N → ℚ) (j : Fin N) :
    (rationalFixedA c u v w j : ℝ) =
      fixedA c (fun j => (u j : ℝ)) (fun j => (v j : ℝ)) (fun j => (w j : ℝ)) j := by
  cases h : c j <;> simp [rationalFixedA, fixedA, h]

@[simp] theorem rationalFreeA_cast (c : Fin N → StateClass) (w : Fin N → ℚ) (j : Fin N) :
    (rationalFreeA c w j : ℝ) = freeA c (fun j => (w j : ℝ)) j := by
  unfold rationalFreeA freeA
  split_ifs <;> simp

def recoverGadget (c : Fin N → StateClass) (u v w : Fin N → ℚ) (xa : ℚ) :
    Vector ℚ N × ℕ :=
  let fixed := Vector.ofFn (rationalFixedA c u v w)
  let capacity := Vector.ofFn (rationalFreeA c w)
  let total := xa - fixed.toList.sum
  let fill := greedyFill capacity.get total
  (Vector.ofFn (fun j => fixed.get j + fill.1 j), fill.2 + 6 * N + 1)

theorem recoverGadget_value (c : Fin N → StateClass) (u v w : Fin N → ℚ) (xa : ℚ)
    (j : Fin N) :
    (recoverGadget c u v w xa).1.get j = rationalFixedA c u v w j +
      (greedyFill (rationalFreeA c w) (xa - ∑ k, rationalFixedA c u v w k)).1 j := by
  have he : (Vector.ofFn (rationalFreeA c w)).get = rationalFreeA c w :=
    funext (fun j => Vector.get_ofFn _ j)
  simp [recoverGadget, Vector.toList_ofFn, List.sum_ofFn, he]

theorem recoverGadget_charge (c : Fin N → StateClass) (u v w : Fin N → ℚ) (xa : ℚ) :
    (recoverGadget c u v w xa).2 = 8 * N + 1 := by
  simp only [recoverGadget, greedyFill_charge]
  omega

theorem recoverGadget_spec (c : Fin N → StateClass) (u v w : Fin N → ℚ) (xa : ℚ)
    (hw : ∀ j, 0 ≤ w j)
    (hn : ObservedNonnegative c (fun j => (u j : ℝ)) (fun j => (v j : ℝ)))
    (h : GadgetProfile c (fun j => (u j : ℝ)) (fun j => (v j : ℝ))
      (fun j => (w j : ℝ)) (xa : ℝ)) :
    (∀ j, 0 ≤ ((recoverGadget c u v w xa).1.get j : ℝ) ∧
      ((recoverGadget c u v w xa).1.get j : ℝ) ≤ (w j : ℝ)) ∧
    (∀ j, observesA (c j) → ((recoverGadget c u v w xa).1.get j : ℝ) = (u j : ℝ)) ∧
    (∀ j, observesB (c j) → (w j : ℝ) - ((recoverGadget c u v w xa).1.get j : ℝ) = v j) ∧
    (∑ j, ((recoverGadget c u v w xa).1.get j : ℝ)) = (xa : ℝ) := by
  obtain ⟨hA, hB, hT, hlo, hhi⟩ := h
  have hfixed : ∀ j, 0 ≤ (rationalFixedA c u v w j : ℝ) ∧
      (rationalFixedA c u v w j : ℝ) + (rationalFreeA c w j : ℝ) ≤ (w j : ℝ) := by
    intro j
    cases hc : c j with
    | aOnly => simpa [rationalFixedA, rationalFreeA, hc] using
        And.intro (hn.1 j (by simp [observesA, hc])) (hA j hc)
    | bOnly =>
        have hv := hn.2 j (by simp [observesB, hc])
        have hbw := hB j hc
        simp only [rationalFixedA, rationalFreeA, hc, reduceCtorEq, ↓reduceIte,
          Rat.cast_sub, Rat.cast_zero, add_zero]
        constructor <;> linarith
    | both =>
        have hu := hn.1 j (by simp [observesA, hc])
        have hv := hn.2 j (by simp [observesB, hc])
        have ht := hT j hc
        simp only [rationalFixedA, rationalFreeA, hc, reduceCtorEq, ↓reduceIte,
          Rat.cast_zero, add_zero]
        exact ⟨hu, by linarith⟩
    | neither => simp [rationalFixedA, rationalFreeA, hc]
  have hfree : ∀ j, 0 ≤ rationalFreeA c w j := by
    intro j
    unfold rationalFreeA
    split_ifs
    · exact hw j
    · exact le_rfl
  have hsum := sum_fixedA c (fun j => (u j : ℝ)) (fun j => (v j : ℝ))
    (fun j => (w j : ℝ))
  have hr0 : 0 ≤ xa - ∑ j, rationalFixedA c u v w j := by
    apply (Rat.cast_nonneg (K := ℝ)).mp
    push_cast
    simp only [rationalFixedA_cast]
    unfold residual at hlo
    linarith
  have hrle : xa - ∑ j, rationalFixedA c u v w j ≤ ∑ j, rationalFreeA c w j := by
    apply (Rat.cast_le (K := ℝ)).mp
    push_cast
    simp only [rationalFixedA_cast, rationalFreeA_cast]
    unfold residual at hhi
    linarith
  obtain ⟨hb, hs⟩ := greedyFill_spec (rationalFreeA c w)
    (xa - ∑ j, rationalFixedA c u v w j) hfree hr0 hrle
  have hbounds (j : Fin N) :
      (rationalFixedA c u v w j : ℝ) ≤ ((recoverGadget c u v w xa).1.get j : ℝ) ∧
      ((recoverGadget c u v w xa).1.get j : ℝ) ≤
        (rationalFixedA c u v w j : ℝ) + (rationalFreeA c w j : ℝ) := by
    rw [recoverGadget_value, Rat.cast_add]
    constructor
    · exact le_add_of_nonneg_right (by exact_mod_cast (hb j).1)
    · gcongr
      exact_mod_cast (hb j).2
  refine ⟨fun j => ⟨(hfixed j).1.trans (hbounds j).1, (hbounds j).2.trans (hfixed j).2⟩,
    ?_, ?_, ?_⟩
  · intro j hj
    have hl := (hbounds j).1
    have hu := (hbounds j).2
    rcases hj with hj | hj <;>
      simp only [rationalFixedA, rationalFreeA, hj, reduceCtorEq, ↓reduceIte,
        Rat.cast_zero, add_zero, Rat.cast_le] at hl hu <;>
      exact_mod_cast le_antisymm hu hl
  · intro j hj
    have hl := (hbounds j).1
    have hu := (hbounds j).2
    rcases hj with hj | hj
    · simp [rationalFixedA, rationalFreeA, hj] at hl hu
      linarith
    · have ht := hT j hj
      simp only [rationalFixedA, rationalFreeA, hj, reduceCtorEq, ↓reduceIte,
        Rat.cast_zero, add_zero, Rat.cast_le] at hl hu
      have he : (recoverGadget c u v w xa).1.get j = u j := le_antisymm hu hl
      rw [he]
      linarith
  · have hQ : (∑ j, (recoverGadget c u v w xa).1.get j) = xa := by
      simp_rw [recoverGadget_value]
      rw [Finset.sum_add_distrib, hs]
      ring
    exact_mod_cast hQ

/-- Materialized state arrays; each gadget's greedy fill is computed once. -/
structure RationalStateFlows (L N : ℕ) where
  a : Vector (Vector ℚ N) L
  b : Vector (Vector ℚ N) L
  h : Vector ℚ N
  work : ℕ

def RationalStateFlows.toReal (f : RationalStateFlows L N) : StateFlows (Fin L) (Fin N) :=
  ⟨fun i j => (f.a.get i).get j, fun i j => (f.b.get i).get j, fun j => f.h.get j⟩

def recoverStateFlows (c : Fin L → Fin N → StateClass) (u v : Fin L → Fin N → ℚ)
    (weights : Fin N → ℚ) (xa : Fin L → ℚ) (w : Fin N → ℚ) : RationalStateFlows L N :=
  let rows := Vector.ofFn (fun i => recoverGadget (c i) (u i) (v i) w (xa i))
  { a := rows.map Prod.fst
    b := Vector.ofFn (fun i => Vector.ofFn (fun j => w j - (rows.get i).1.get j))
    h := Vector.ofFn (fun j => weights j - w j)
    work := (∑ i, (rows.get i).2) + L * N + N }

@[simp] theorem recoverStateFlows_a (c : Fin L → Fin N → StateClass)
    (u v : Fin L → Fin N → ℚ) (weights : Fin N → ℚ) (xa : Fin L → ℚ)
    (w : Fin N → ℚ) (i : Fin L) (j : Fin N) :
    ((recoverStateFlows c u v weights xa w).a.get i).get j =
      (recoverGadget (c i) (u i) (v i) w (xa i)).1.get j := by
  simp [recoverStateFlows]

@[simp] theorem recoverStateFlows_b (c : Fin L → Fin N → StateClass)
    (u v : Fin L → Fin N → ℚ) (weights : Fin N → ℚ) (xa : Fin L → ℚ)
    (w : Fin N → ℚ) (i : Fin L) (j : Fin N) :
    ((recoverStateFlows c u v weights xa w).b.get i).get j =
      w j - (recoverGadget (c i) (u i) (v i) w (xa i)).1.get j := by
  simp [recoverStateFlows]

@[simp] theorem recoverStateFlows_h (c : Fin L → Fin N → StateClass)
    (u v : Fin L → Fin N → ℚ) (weights : Fin N → ℚ) (xa : Fin L → ℚ)
    (w : Fin N → ℚ) (j : Fin N) :
    (recoverStateFlows c u v weights xa w).h.get j = weights j - w j := by
  simp [recoverStateFlows]

theorem recoverStateFlows_charge (c : Fin L → Fin N → StateClass)
    (u v : Fin L → Fin N → ℚ) (weights : Fin N → ℚ) (xa : Fin L → ℚ) (w : Fin N → ℚ) :
    (recoverStateFlows c u v weights xa w).work = L * (9 * N + 1) + N := by
  simp [recoverStateFlows, recoverGadget_charge]
  ring

/-- The actual cached output satisfies every state-flow equation and observation. -/
theorem recoverStateFlows_spec (c : Fin L → Fin N → StateClass)
    (u v : Fin L → Fin N → ℚ) (weights : Fin N → ℚ) (xa xb : Fin L → ℚ)
    (xh : ℚ) (observedH : Fin N → Prop) (zh w : Fin N → ℚ)
    (hweights : ∑ j, weights j = 1) (haggregate : ∀ i, xa i + xb i = 1 - xh)
    (hn : ∀ i, ObservedNonnegative (c i) (fun j => (u i j : ℝ)) (fun j => (v i j : ℝ)))
    (hp : Profile c (fun i j => (u i j : ℝ)) (fun i j => (v i j : ℝ))
      (fun j => (weights j : ℝ)) (fun i => (xa i : ℝ)) xh observedH
      (fun j => (zh j : ℝ)) (fun j => (w j : ℝ))) :
    ValidStateFlows c (fun i j => (u i j : ℝ)) (fun i j => (v i j : ℝ))
      (fun j => (weights j : ℝ)) (fun i => (xa i : ℝ)) (fun i => (xb i : ℝ))
      xh observedH (fun j => (zh j : ℝ))
      (recoverStateFlows c u v weights xa w).toReal := by
  obtain ⟨hw, hsumw, hH, hg⟩ := hp
  have hfill i := recoverGadget_spec (c i) (u i) (v i) w (xa i)
    (fun j => by have h : (0 : ℝ) ≤ (w j : ℝ) := (hw j).1; exact_mod_cast h) (hn i) (hg i)
  have ha (i : Fin L) (j : Fin N) :
      0 ≤ ((recoverGadget (c i) (u i) (v i) w (xa i)).1.get j : ℝ) ∧
      ((recoverGadget (c i) (u i) (v i) w (xa i)).1.get j : ℝ) ≤ w j := (hfill i).1 j
  have hsum (i : Fin L) : (∑ j,
      ((recoverGadget (c i) (u i) (v i) w (xa i)).1.get j : ℝ)) = xa i := (hfill i).2.2.2
  simp only [ValidStateFlows, RationalStateFlows.toReal, recoverStateFlows_a,
    recoverStateFlows_b, recoverStateFlows_h, Rat.cast_sub]
  refine ⟨?_, ?_, ?_, ?_, hsum, ?_, ?_, ?_, ?_, ?_⟩
  · intro i j
    exact ⟨(ha i j).1, (ha i j).2.trans (hw j).2⟩
  · intro i j
    constructor <;> linarith [(ha i j).1, (ha i j).2, (hw j).2]
  · intro j
    constructor <;> linarith [(hw j).1, (hw j).2]
  · intro i j
    ring
  · intro i
    rw [Finset.sum_sub_distrib, hsumw, hsum i]
    have hi : (xa i : ℝ) + (xb i : ℝ) = 1 - (xh : ℝ) := by exact_mod_cast haggregate i
    linarith
  · rw [Finset.sum_sub_distrib, hsumw]
    have ht : (∑ j, (weights j : ℝ)) = 1 := by exact_mod_cast hweights
    rw [ht]
    ring
  · exact fun i => (hfill i).2.1
  · exact fun i => (hfill i).2.2.1
  · intro j hj
    linarith [hH j hj]

/-- No state normalization is needed for reconstruction; zero weights force zero output. -/
theorem recoverStateFlows_zero_weight (c : Fin L → Fin N → StateClass)
    (u v : Fin L → Fin N → ℚ) (weights : Fin N → ℚ) (xa xb : Fin L → ℚ)
    (xh : ℚ) (observedH : Fin N → Prop) (zh w : Fin N → ℚ)
    (hweights : ∑ j, weights j = 1) (haggregate : ∀ i, xa i + xb i = 1 - xh)
    (hn : ∀ i, ObservedNonnegative (c i) (fun j => (u i j : ℝ)) (fun j => (v i j : ℝ)))
    (hp : Profile c (fun i j => (u i j : ℝ)) (fun i j => (v i j : ℝ))
      (fun j => (weights j : ℝ)) (fun i => (xa i : ℝ)) xh observedH
      (fun j => (zh j : ℝ)) (fun j => (w j : ℝ))) (j : Fin N) (hj : weights j = 0) :
    (recoverStateFlows c u v weights xa w).h.get j = 0 ∧
      ∀ i, ((recoverStateFlows c u v weights xa w).a.get i).get j = 0 ∧
        ((recoverStateFlows c u v weights xa w).b.get i).get j = 0 := by
  have h := zero_weight_entries c (fun i j => (u i j : ℝ)) (fun i j => (v i j : ℝ))
    (fun j => (weights j : ℝ)) (fun i => (xa i : ℝ)) (fun i => (xb i : ℝ))
    xh observedH (fun j => (zh j : ℝ)) _
    (recoverStateFlows_spec c u v weights xa xb xh observedH zh w hweights haggregate hn hp)
    j (by simp [hj])
  dsimp only [RationalStateFlows.toReal] at h
  constructor
  · exact_mod_cast h.1
  · intro i
    constructor
    · exact_mod_cast (h.2 i).1
    · exact_mod_cast (h.2 i).2

end NetworkSimplex.Chain
