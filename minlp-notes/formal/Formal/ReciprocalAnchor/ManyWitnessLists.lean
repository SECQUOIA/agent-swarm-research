import Mathlib.Data.List.OfFn
import Mathlib.Data.Rat.Defs

/-! Materializing the product coordinates of finite rational graph witnesses. -/
namespace ReciprocalAnchor.ManyLeaf

theorem zipWith_mul_ofFn {K : ℕ} (x y : Fin K → ℚ) :
    List.zipWith (· * ·) (List.ofFn x) (List.ofFn y) =
      List.ofFn (fun i => x i * y i) := by
  apply List.ext_getElem <;> simp

end ReciprocalAnchor.ManyLeaf
