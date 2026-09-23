import Formal.NetworkSimplex.ThresholdRationalRows
import Formal.NetworkSimplex.ProfileHull

/-! Executable rational original-domain prechecks with their exact real meaning. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

namespace RationalData
variable {m L : ℕ}

def oppositeFlow (D : RationalData m L) (i : Fin L) : ℚ := 1 - D.xh - D.xa i

/-- The original flow balance is already built into `oppositeFlow`. -/
def DomainChecks (D : RationalData m L) : Prop :=
  (∀ j, 0 ≤ D.weights j) ∧ (List.ofFn D.weights).sum = 1 ∧
  (0 ≤ D.xh ∧ D.xh ≤ 1) ∧
  (∀ i, (0 ≤ D.xa i ∧ D.xa i ≤ 1) ∧
    (0 ≤ D.oppositeFlow i ∧ D.oppositeFlow i ≤ 1)) ∧
  (∀ i j, observesA (D.c i j) → 0 ≤ D.u i j) ∧
  (∀ i j, observesB (D.c i j) → 0 ≤ D.v i j) ∧
  (∀ j, D.observedH j = true → 0 ≤ D.zh j)

instance (D : RationalData m L) : Decidable D.DomainChecks := by
  unfold DomainChecks
  infer_instance

def domainCheck (D : RationalData m L) : Bool := decide D.DomainChecks

@[simp] theorem oppositeFlow_cast (D : RationalData m L) (i : Fin L) :
    (D.oppositeFlow i : ℝ) = D.toReal.xb i := by
  simp [oppositeFlow, ReductionData.xb, toReal]

theorem domainChecks_iff (D : RationalData m L) : D.DomainChecks ↔ D.toReal.OriginalDomain := by
  constructor
  · rintro ⟨hw, hs, hh, hab, hu, hv, hz⟩
    refine ⟨⟨?_, ?_⟩, ?_, ?_, ?_⟩
    · intro j; change 0 ≤ (D.weights j : ℝ); exact_mod_cast hw j
    · change ∑ j, (D.weights j : ℝ) = 1
      simpa only [List.sum_ofFn, Rat.cast_sum, Rat.cast_one] using
        congrArg (fun q : ℚ => (q : ℝ)) hs
    · apply (flow_iff L _ 1).mpr
      constructor
      · intro e
        rcases e with ⟨i, f⟩ | u
        · cases f
          · simpa only [pack, toReal] using
              (show 0 ≤ (D.xa i : ℝ) ∧ (D.xa i : ℝ) ≤ 1 by exact_mod_cast (hab i).1)
          · simpa only [pack, ← oppositeFlow_cast] using
              (show 0 ≤ (D.oppositeFlow i : ℝ) ∧ (D.oppositeFlow i : ℝ) ≤ 1 by
                exact_mod_cast (hab i).2)
        · simpa only [pack, toReal] using
            (show 0 ≤ (D.xh : ℝ) ∧ (D.xh : ℝ) ≤ 1 by exact_mod_cast hh)
      · intro i
        simp only [pack_a, pack_b, pack_bypass, ReductionData.xb]
        ring
    · intro i
      constructor
      · intro j h
        change 0 ≤ (D.u i j : ℝ)
        exact_mod_cast hu i j h
      · intro j h
        change 0 ≤ (D.v i j : ℝ)
        exact_mod_cast hv i j h
    · intro j h; change 0 ≤ (D.zh j : ℝ); exact_mod_cast hz j h
  · rintro ⟨⟨hw, hs⟩, hf, hn, hz⟩
    dsimp only [toReal] at hw hs hn hz
    have hflow := (flow_iff L _ 1).mp hf
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · intro j; exact_mod_cast hw j
    · have h : ((List.ofFn D.weights).sum : ℝ) = 1 := by
        simpa only [List.sum_ofFn, Rat.cast_sum] using hs
      exact_mod_cast h
    · have h := hflow.1 bypass
      simp only [pack_bypass, toReal] at h
      exact_mod_cast h
    · intro i
      have ha := hflow.1 (a i)
      have hb := hflow.1 (b i)
      simp only [pack_a, toReal] at ha
      simp only [pack_b, ← oppositeFlow_cast] at hb
      exact ⟨by exact_mod_cast ha, by exact_mod_cast hb⟩
    · intro i j h
      have hh : 0 ≤ (D.u i j : ℝ) := (hn i).1 j h
      exact_mod_cast hh
    · intro i j h
      have hh : 0 ≤ (D.v i j : ℝ) := (hn i).2 j h
      exact_mod_cast hh
    · intro j h; exact_mod_cast hz j h

@[simp] theorem domainCheck_eq_true (D : RationalData m L) :
    D.domainCheck = true ↔ D.toReal.OriginalDomain := by
  simp only [domainCheck, decide_eq_true_eq, domainChecks_iff]

/-- A generic exact hull admission wrapper after the original-domain checks. -/
def hullCheck (D : RationalData m L) (profileAccepted : Bool) : Bool :=
  D.domainCheck && profileAccepted

theorem hullCheck_eq_true (D : RationalData m L) (profileAccepted : Bool)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (hp : profileAccepted = true ↔ ∃ x, D.toReal.ReducedProfile x) :
    D.hullCheck profileAccepted = true ↔ D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph := by
  rw [hullCheck, Bool.and_eq_true, domainCheck_eq_true, hp, D.toReal.mem_hull_iff,
    D.toReal.exists_fullProfile_iff_rows hc hh]
  exact and_congr_right fun _ => (exists_congr fun x => D.toReal.rows_iff_reducedProfile x).symm

end RationalData
end NetworkSimplex.Chain.Threshold
