import Formal.DAGSpectral.DyadicScale
import Formal.DAGSpectral.BitComplexity

namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

theorem dyadicSearch_bits {w q : ℚ} {K : ℕ} (hq : RationalBits q K) (n : ℕ) :
    RationalBits (dyadicSearch w n q) (K+2*n) := by
  induction n generalizing q K with
  | zero => simpa [dyadicSearch] using hq
  | succ n ih =>
    simp only [dyadicSearch]
    split_ifs
    · exact rationalBits_mono hq (by omega)
    · convert ih (rationalBits_mul rationalBits_two hq) using 1
      omega

theorem dyadicScale_bits (w : ℚ) (B : ℕ) :
    RationalBits (dyadicScale w B) (6*B+1) := by
  have h := dyadicSearch_bits (w := w) (rationalBits_inv (rationalBits_two_pow B)) (2*B)
  unfold dyadicScale
  convert h using 1
  omega

/-- The exact arithmetic-event trace of the bounded rational scale scan. -/
def dyadicTrace (w : ℚ) : ℕ → ℚ → List ArithmeticEvent
  | 0, _ => []
  | n+1, q => [(.mul,q,q),(.mul,q*q,w),(.compare,1,q*q*w)] ++
      if 1 ≤ q^2*w then [] else (.mul,2,q) :: dyadicTrace w n (2*q)

theorem dyadicTrace_length (w q : ℚ) (n : ℕ) : (dyadicTrace w n q).length ≤ 4*n := by
  induction n generalizing q with
  | zero => simp [dyadicTrace]
  | succ n ih =>
    simp only [dyadicTrace,List.length_append]
    split_ifs <;> simp only [List.length_cons,List.length_nil]
    · omega
    · have h := ih (2*q); omega

theorem dyadicTrace_bits {w q : ℚ} {B K : ℕ}
    (hw : RationalBits w B) (hq : RationalBits q K) (n : ℕ) :
    ∀ e ∈ dyadicTrace w n q, eventBits (2*(K+2*n)+B+2) e := by
  induction n generalizing q K with
  | zero => simp [dyadicTrace]
  | succ n ih =>
    intro e he
    have hq' : RationalBits q (2*(K+2*(n+1))+B+2) := rationalBits_mono hq (by omega)
    have hw' : RationalBits w (2*(K+2*(n+1))+B+2) := rationalBits_mono hw (by omega)
    have hs : RationalBits (q*q) (2*(K+2*(n+1))+B+2) :=
      rationalBits_mono (rationalBits_mul hq hq) (by omega)
    have hp : RationalBits (q*q*w) (2*(K+2*(n+1))+B+2) :=
      rationalBits_mono (rationalBits_mul (rationalBits_mul hq hq) hw) (by omega)
    have h1 : RationalBits 1 (2*(K+2*(n+1))+B+2) := rationalBits_mono rationalBits_one (by omega)
    have h2 : RationalBits 2 (2*(K+2*(n+1))+B+2) := rationalBits_mono rationalBits_two (by omega)
    simp only [dyadicTrace,List.mem_append,List.mem_cons,List.not_mem_nil,or_false] at he
    rcases he with (rfl|rfl|rfl) | he
    · exact ⟨hq',hq'⟩
    · exact ⟨hs,hw'⟩
    · exact ⟨h1,hp⟩
    · split_ifs at he
      · simp at he
      · rcases List.mem_cons.mp he with rfl | he
        · exact ⟨h2,hq'⟩
        · have h := ih (rationalBits_mul rationalBits_two hq) e he
          convert h using 1
          congr 1
          omega

/-- Successive doubling is an explicit way to compute the initial power. -/
def powerTwoTrace : ℕ → List ArithmeticEvent
  | 0 => []
  | n+1 => powerTwoTrace n ++ [(.mul,(2:ℚ)^n,2)]

theorem powerTwoTrace_length (n : ℕ) : (powerTwoTrace n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [powerTwoTrace,ih]

theorem powerTwoTrace_bits (n : ℕ) :
    ∀ e ∈ powerTwoTrace n, eventBits (2*n+2) e := by
  induction n with
  | zero => simp [powerTwoTrace]
  | succ n ih =>
    intro e he
    simp only [powerTwoTrace,List.mem_append,List.mem_singleton] at he
    rcases he with he | rfl
    · exact ⟨rationalBits_mono (ih e he).1 (by omega),
        rationalBits_mono (ih e he).2 (by omega)⟩
    · exact ⟨rationalBits_mono (rationalBits_two_pow n) (by omega),
        rationalBits_mono rationalBits_two (by omega)⟩

def dyadicScaleTrace (w : ℚ) (B : ℕ) : List ArithmeticEvent :=
  powerTwoTrace B ++ [(.inv,(2:ℚ)^B,0)] ++ dyadicTrace w (2*B) ((2:ℚ)^B)⁻¹

theorem dyadicScaleTrace_length (w : ℚ) (B : ℕ) :
    (dyadicScaleTrace w B).length ≤ 9*B+1 := by
  have h := dyadicTrace_length w ((2:ℚ)^B)⁻¹ (2*B)
  simp only [dyadicScaleTrace,List.length_append,powerTwoTrace_length,
    List.length_cons,List.length_nil]
  omega

theorem dyadicScaleTrace_bits {w : ℚ} {B : ℕ} (hw : RationalBits w B) :
    ∀ e ∈ dyadicScaleTrace w B, eventBits (13*B+4) e := by
  intro e he
  simp only [dyadicScaleTrace,List.mem_append,List.mem_singleton] at he
  rcases he with (he|rfl) | he
  · exact ⟨rationalBits_mono (powerTwoTrace_bits B e he).1 (by omega),
      rationalBits_mono (powerTwoTrace_bits B e he).2 (by omega)⟩
  · exact ⟨rationalBits_mono (rationalBits_two_pow B) (by omega),
      rationalBits_mono rationalBits_zero (by omega)⟩
  · have h := dyadicTrace_bits hw (rationalBits_inv (rationalBits_two_pow B)) (2*B) e he
    have heq : 2*(2*B+1+2*(2*B))+B+2 = 13*B+4 := by omega
    rw [heq] at h
    exact h

/-- Actual arithmetic trace cost is polynomial in the rational input bit bound.
Large dyadic exponents increase bit length, not the number of DP labels. -/
theorem dyadicScale_bitWork {w : ℚ} {B : ℕ} (hw : RationalBits w B) :
    traceBitWork (13*B+4) (dyadicScaleTrace w B) ≤
      (9*B+1) * (256 * (13*B+5)^3) := by
  apply (traceBitWork_le (dyadicScaleTrace_bits hw)).trans
  apply Nat.mul_le_mul (dyadicScaleTrace_length w B)
  rfl

/-- Coupled execution of successive doubling and its actual arithmetic events. -/
def powerTwoRun : ℕ → ℚ × List ArithmeticEvent
  | 0 => (1,[])
  | n+1 =>
    let previous := powerTwoRun n
    (previous.1*2,previous.2 ++ [(.mul,previous.1,2)])

theorem powerTwoRun_spec (n : ℕ) :
    powerTwoRun n = ((2:ℚ)^n,powerTwoTrace n) := by
  induction n with
  | zero => simp [powerTwoRun,powerTwoTrace]
  | succ n ih => simp [powerTwoRun,ih,powerTwoTrace,pow_succ]

/-- The scale and trace are produced together, with each square/product reused
for the branch decision. Fuel bounds every execution, including invalid inputs. -/
def dyadicSearchRun (w : ℚ) : ℕ → ℚ → ℚ × List ArithmeticEvent
  | 0, q => (q,[])
  | n+1, q =>
    let squared := q*q
    let tested := squared*w
    let eventsHead : List ArithmeticEvent := [(.mul,q,q),(.mul,squared,w),(.compare,1,tested)]
    if 1 ≤ tested then (q,eventsHead)
    else
      let next := dyadicSearchRun w n (2*q)
      (next.1,eventsHead ++ (.mul,2,q)::next.2)

theorem dyadicSearchRun_spec (w q : ℚ) (n : ℕ) :
    dyadicSearchRun w n q = (dyadicSearch w n q,dyadicTrace w n q) := by
  induction n generalizing q with
  | zero => rfl
  | succ n ih =>
    simp only [dyadicSearchRun,dyadicSearch,dyadicTrace,pow_two]
    split_ifs <;> simp [ih]

/-- Callable dyadic normalization returning both the value and its executed
rational-operation trace. -/
def dyadicScaleRun (w : ℚ) (B : ℕ) : ℚ × List ArithmeticEvent :=
  let powered := powerTwoRun B
  let initial := powered.1⁻¹
  let result := dyadicSearchRun w (2*B) initial
  (result.1,powered.2 ++ [(.inv,powered.1,0)] ++ result.2)

theorem dyadicScaleRun_spec (w : ℚ) (B : ℕ) :
    dyadicScaleRun w B = (dyadicScale w B,dyadicScaleTrace w B) := by
  simp [dyadicScaleRun,powerTwoRun_spec,dyadicSearchRun_spec,dyadicScale,dyadicScaleTrace]

end DAGSpectral
