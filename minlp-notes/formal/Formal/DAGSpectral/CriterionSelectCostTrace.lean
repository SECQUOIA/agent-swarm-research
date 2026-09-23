import Formal.DAGSpectral.CriterionSelectContrast
import Formal.DAGSpectral.CriterionSelectTrace

namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

/-- Explicit max and order comparisons for finite rational costs. -/
def rationalCostLERun (a b : Option ℚ) : Bool × List ArithmeticEvent :=
  match a,b with
  | some x,some y =>
    let clippedX := if x ≤ 0 then 0 else x
    let clippedY := if y ≤ 0 then 0 else y
    (decide (clippedX ≤ clippedY),
      [(.compare,x,0),(.compare,y,0),(.compare,clippedX,clippedY)])
  | _,none => (true,[])
  | none,some _ => (false,[])

@[simp] theorem rationalCostLERun_value (a b : Option ℚ) :
    (rationalCostLERun a b).1 = rationalCostLE a b := by
  cases a <;> cases b <;> simp [rationalCostLERun,rationalCostLE,max_def]

def optionalRationalBits (v : Option ℚ) (B : ℕ) : Prop := ∀ q ∈ v, RationalBits q B

theorem rationalCostLERun_bounds {a b : Option ℚ} {B : ℕ} (hB : 0 < B)
    (ha : optionalRationalBits a B) (hb : optionalRationalBits b B) :
    (rationalCostLERun a b).2.length ≤ 3 ∧
      ∀ e ∈ (rationalCostLERun a b).2, eventBits B e := by
  have hz : RationalBits 0 B := rationalBits_mono rationalBits_zero hB
  cases a with
  | none => cases b <;> simp [rationalCostLERun]
  | some x =>
    cases b with
    | none => simp [rationalCostLERun]
    | some y =>
      have hx := ha x (by simp)
      have hy := hb y (by simp)
      have hmx : RationalBits (max x 0) B := by
        rcases le_total x 0 with h|h
        · simpa only [max_eq_right h] using hz
        · simpa only [max_eq_left h] using hx
      have hmy : RationalBits (max y 0) B := by
        rcases le_total y 0 with h|h
        · simpa only [max_eq_right h] using hz
        · simpa only [max_eq_left h] using hy
      refine ⟨by simp [rationalCostLERun],?_⟩
      intro e he
      simp only [rationalCostLERun,← max_def,List.mem_cons,List.not_mem_nil,or_false] at he
      rcases he with rfl|rfl|rfl
      · exact ⟨hx,hz⟩
      · exact ⟨hy,hz⟩
      · exact ⟨hmx,hmy⟩

end DAGSpectral
