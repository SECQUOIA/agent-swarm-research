import Mathlib.Data.Rat.Cast.Defs
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Fin.VecNotation
import Mathlib.Algebra.BigOperators.Fin

namespace CubicGap

/-- The six orbit contributions evaluated at success counts. -/
def countPhi (coef : Fin 6 → ℚ) (a b c : ℕ) : ℚ :=
  coef 0 * (c.choose 3 : ℚ) + coef 1 * b * (c.choose 2 : ℚ) +
    coef 2 * (b.choose 2 : ℚ) + coef 3 * a * c + coef 4 * a * b +
    coef 5 * (a.choose 2 : ℚ)

def coefficients6 : Fin 6 → ℚ := ![2, 3, 9, 10, 7, 7]
def coefficients8 : Fin 6 → ℚ := ![2, 3, 13, 12, 8, 7]
def coefficients64 : Fin 6 → ℚ := ![2, 3, 120, 105, 70, 63]

def threeValue6 := countPhi coefficients6
def threeValue8 := countPhi coefficients8
def threeValue64 := countPhi coefficients64

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive finite checking requires removing the tactic heartbeat limit.
/-- Every count triple for the 18-variable example satisfies its affine bound.
Kernel reduction checks the finite rational inequalities. -/
theorem minorant6 : ∀ a b c : Fin 7,
    (962 * (a : ℚ) + 778 * (b : ℚ) + 842 * (c : ℚ) - 4816) / 13 ≤
      threeValue6 a b c := by
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive finite checking requires removing the tactic heartbeat limit.
/-- Every count triple for the 24-variable example satisfies its affine bound.
Kernel reduction checks the finite rational inequalities. -/
theorem minorant8 : ∀ a b c : Fin 9,
    (793 * (a : ℚ) + 770 * (b : ℚ) + 798 * (c : ℚ) - 5882) / 7 ≤
      threeValue8 a b c := by
  decide +kernel

/-- Two-group count polynomial, including the homogeneous fixed coordinates. -/
def twoValue (m a c : ℕ) : ℚ :=
  a * (c.choose 2 : ℚ) + (5 * (m : ℚ) / 4) * (a.choose 2 : ℚ)

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive finite checking requires removing the tactic heartbeat limit.
/-- Finite rational verification of all 25 count pairs. -/
theorem two_minorant4 : ∀ a c : Fin 5,
    9 * (a : ℚ) + 4 * (c : ℚ) - 19 ≤ twoValue 4 a c := by
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive finite checking requires removing the tactic heartbeat limit.
/-- Finite rational verification of all 81 count pairs. -/
theorem two_minorant8 : ∀ a c : Fin 9,
    47 * (a : ℚ) + 20 * (c : ℚ) - 188 ≤ twoValue 8 a c := by
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive finite checking requires removing the tactic heartbeat limit.
/-- Finite rational verification of all 169 count pairs. -/
theorem two_minorant12 : ∀ a c : Fin 13,
    (231 / 2 : ℚ) * (a : ℚ) + 48 * (c : ℚ) - 684 ≤ twoValue 12 a c := by
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive finite checking requires removing the tactic heartbeat limit.
/-- Finite rational verification of all 289 count pairs. -/
theorem two_minorant16 : ∀ a c : Fin 17,
    214 * (a : ℚ) + (177 / 2 : ℚ) * (c : ℚ) - 1686 ≤ twoValue 16 a c := by
  decide +kernel

/-- Listed count laws. Their support dimensions enforce the advertised count bounds. -/
def states6 : Fin 3 → Fin 3 → Fin 7 := ![![1,4,4], ![2,1,6], ![6,2,1]]
def weights6 : Fin 3 → ℚ := ![17/26, 8/26, 1/26]
def states8 : Fin 3 → Fin 3 → Fin 9 := ![![1,2,8], ![1,5,6], ![8,4,2]]
def weights8 : Fin 3 → ℚ := ![2/7, 4/7, 1/7]
def states64 : Fin 4 → Fin 3 → Fin 65 :=
  ![![4,19,64], ![5,19,64], ![16,40,43], ![64,31,17]]
def weights64 : Fin 4 → ℚ := ![241/735, 12/735, 419/735, 63/735]

/-- All data needed to take expectations under the explicit count law. -/
def PrimalLaw {k m : ℕ} (states : Fin k → Fin 3 → Fin (m + 1))
    (weights : Fin k → ℚ) (value : ℕ → ℕ → ℕ → ℚ) (objective : ℚ) : Prop :=
  (∀ i, 0 ≤ weights i) ∧ (∑ i, weights i) = 1 ∧
  (∀ j, (∑ i, weights i * (states i j : ℚ)) =
    ![(m : ℚ)/4, (m : ℚ)/2, 3*(m : ℚ)/4] j) ∧
  (∑ i, weights i * value (states i 0) (states i 1) (states i 2)) = objective

instance {k m : ℕ} (s : Fin k → Fin 3 → Fin (m + 1)) (w : Fin k → ℚ)
    (v : ℕ → ℕ → ℕ → ℚ) (q : ℚ) : Decidable (PrimalLaw s w v q) := by
  unfold PrimalLaw
  infer_instance

theorem primal6 : PrimalLaw states6 weights6 threeValue6 (2750/13) := by decide +kernel
theorem primal8 : PrimalLaw states8 weights8 threeValue8 (3572/7) := by decide +kernel
theorem primal64 : PrimalLaw states64 weights64 threeValue64 (34172072/105) := by
  decide +kernel

/-- Sum of upper values for the six monomial orbits. -/
def orbitUpper (m : ℕ) (coef : Fin 6 → ℚ) : ℚ :=
  coef 0 * (m.choose 3 : ℚ) * (3/4) +
  coef 1 * m * (m.choose 2 : ℚ) * (1/2) +
  coef 2 * (m.choose 2 : ℚ) * (1/2) +
  coef 3 * m * m * (1/4) + coef 4 * m * m * (1/4) +
  coef 5 * (m.choose 2 : ℚ) * (1/4)

def orbitLower (m : ℕ) (coef : Fin 6 → ℚ) : ℚ :=
  coef 0 * (m.choose 3 : ℚ) / 4

theorem arithmetic6 :
    orbitUpper 6 coefficients6 = 1647/4 ∧ orbitLower 6 coefficients6 = 10 ∧
    ((962*(6/4) + 778*(6/2) + 842*(3*6/4)-4816)/13 : ℚ) = 2750/13 ∧
    (1647/4 - 2750/13 : ℚ) = 10411/52 ∧
    ((1647/4 - 10)/(1647/4 - 2750/13) : ℚ) = 20891/10411 ∧
    (2 : ℚ) < 20891/10411 := by decide +kernel

theorem arithmetic8 :
    orbitUpper 8 coefficients8 = 971 ∧ orbitLower 8 coefficients8 = 28 ∧
    ((793*(8/4) + 770*(8/2) + 798*(3*8/4)-5882)/7 : ℚ) = 3572/7 ∧
    (971 - 3572/7 : ℚ) = 3225/7 ∧
    ((971 - 28)/(971 - 3572/7) : ℚ) = 6601/3225 ∧
    (2 : ℚ) < 6601/3225 := by decide +kernel

theorem arithmetic64 :
    orbitUpper 64 coefficients64 = 587944 ∧ orbitLower 64 coefficients64 = 20832 ∧
    ((871710*(64/4) + 900446*(64/2) + 899046*(3*64/4)-51743768)/105 : ℚ) =
      34172072/105 ∧
    (587944 - 34172072/105 : ℚ) = 27562048/105 ∧
    ((587944 - 20832)/(587944 - 34172072/105) : ℚ) = 7443345/3445256 ∧
    (2 : ℚ) < 7443345/3445256 := by decide +kernel

def twoUpper (m : ℕ) : ℚ := (9 * m / 8 : ℚ) * (m.choose 2 : ℚ)

theorem two_arithmetic4 :
    twoValue 4 2 3 = 11 ∧ (9*2+4*3-19 : ℚ) = 11 ∧ twoUpper 4 = 27 ∧
    (27/(27-11) : ℚ) = 27/16 ∧ (27/16 : ℚ) < 2 := by decide +kernel

theorem two_arithmetic8 :
    twoValue 8 4 6 = 120 ∧ (47*4+20*6-188 : ℚ) = 120 ∧ twoUpper 8 = 252 ∧
    (252/(252-120) : ℚ) = 21/11 ∧ (21/11 : ℚ) < 2 := by decide +kernel

theorem two_arithmetic12 :
    twoValue 12 6 9 = 441 ∧ ((231/2)*6+48*9-684 : ℚ) = 441 ∧ twoUpper 12 = 891 ∧
    (891/(891-441) : ℚ) = 99/50 ∧ (99/50 : ℚ) < 2 := by decide +kernel

theorem two_arithmetic16 :
    twoValue 16 8 12 = 1088 ∧ (214*8+(177/2)*12-1686 : ℚ) = 1088 ∧
    twoUpper 16 = 2160 ∧ (2160/(2160-1088) : ℚ) = 135/67 ∧
    (2 : ℚ) < 135/67 := by decide +kernel

end CubicGap
