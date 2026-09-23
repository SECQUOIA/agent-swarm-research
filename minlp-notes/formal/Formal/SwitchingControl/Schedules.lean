import Mathlib

namespace SwitchingControl

/-- Fixed-length lists of modes form a finite set, including empty schedules. -/
instance finite_fixed_words (n : ℕ) : Finite {w : List (Fin 3) // w.length = n} := by
  let encode : {w : List (Fin 3) // w.length = n} → (Fin n → Fin 3) :=
    fun w j => w.val[j.val]'(by rw [w.property]; exact j.isLt)
  apply Finite.of_injective encode
  intro a b hab
  apply Subtype.ext
  apply List.ext_getElem
  · rw [a.property, b.property]
  · intro j hja hjb
    exact congrFun hab ⟨j, by rwa [a.property] at hja⟩

end SwitchingControl
