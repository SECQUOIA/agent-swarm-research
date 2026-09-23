import Formal.DAGSpectral.SpectralAlgorithmCost
import Mathlib.Data.Nat.Choose.Bounds

/-! Uniform polynomial bounds for trial enumeration and retained profile states.
The exponent depends only on the original matrix dimension. -/
namespace DAGSpectral
namespace CoverSizePolynomial
open scoped BigOperators

def upperDimension (p : ℕ) : ℕ := p*(p+1)/2

def uniformCapacity (p v T : ℕ) : ℕ :=
  2^p * (8*p*p*(v+1)^2*T+v+3)^(upperDimension p)

theorem upperDimension_mono {r p : ℕ} (hr : r ≤ p) :
    upperDimension r ≤ upperDimension p := by
  unfold upperDimension
  exact Nat.div_le_div_right (Nat.mul_le_mul hr (Nat.add_le_add_right hr 1))

theorem uniformCapacity_bound {r p v T : ℕ} (hr : r ≤ p) :
    2^r * (8*p*r*(max 1 (v-1))^2*T+max 1 (v-1)+2)^(r*(r+1)/2) ≤
      uniformCapacity p v T := by
  have hN : max 1 (v-1) ≤ v+1 := by omega
  have hb : 8*p*r*(max 1 (v-1))^2*T+max 1 (v-1)+2 ≤
      8*p*p*(v+1)^2*T+v+3 := by
    have hh : 8*p*r*(max 1 (v-1))^2*T ≤ 8*p*p*(v+1)^2*T := by gcongr
    omega
  unfold uniformCapacity
  apply Nat.mul_le_mul (Nat.pow_le_pow_right (by decide) hr)
  exact (Nat.pow_le_pow_left hb _).trans
    (Nat.pow_le_pow_right (by omega) (upperDimension_mono hr))

theorem choose_bound {M r p : ℕ} (hr : r ≤ p) :
    M.choose r ≤ (M+1)^p :=
  (Nat.choose_le_pow M r).trans ((Nat.pow_le_pow_left (by omega : M ≤ M+1) r).trans
    (Nat.pow_le_pow_right (by omega) hr))

theorem chooseSum_bound (M p : ℕ) :
    (∑ r : Fin p, M.choose (r.val+1)) ≤ p*(M+1)^p := by
  calc
    _ ≤ ∑ _r : Fin p, (M+1)^p := Finset.sum_le_sum fun r _ => choose_bound (by omega)
    _ = _ := by simp

def capacityCoefficient (p : ℕ) : ℕ := 2^p*(8*p*p+3)^(upperDimension p)
def capacityDegree (p : ℕ) : ℕ := 3*upperDimension p

theorem uniformCapacity_polynomial (p v T : ℕ) :
    uniformCapacity p v T ≤ capacityCoefficient p * (v+T+1)^(capacityDegree p) := by
  let x := v+T+1
  have hx : 1 ≤ x := by dsimp [x]; omega
  have hv : v+1 ≤ x := by dsimp [x]; omega
  have hT : T ≤ x := by dsimp [x]; omega
  have hx3 : x ≤ x^3 := by
    simpa using (Nat.pow_le_pow_right hx (show 1 ≤ 3 by decide))
  have hm : (v+1)^2*T ≤ x^3 := by
    calc
      _ ≤ x^2*x := Nat.mul_le_mul (Nat.pow_le_pow_left hv 2) hT
      _ = x^3 := by ring
  have hv3 : v+3 ≤ 3*x^3 := by omega
  have hb : 8*p*p*(v+1)^2*T+v+3 ≤ (8*p*p+3)*x^3 := by
    have := Nat.mul_le_mul_left (8*p*p) hm
    nlinarith
  unfold uniformCapacity capacityCoefficient capacityDegree
  calc
    _ ≤ 2^p*((8*p*p+3)*x^3)^(upperDimension p) :=
      Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hb _)
    _ = _ := by rw [mul_pow, ← pow_mul]; dsimp [x]; ring

def candidateCoefficient (p : ℕ) : ℕ := p

theorem trialCapacitySum_polynomial (p M v T : ℕ) :
    (∑ r : Fin p, M.choose (r.val+1) *
      (2^(r.val+1) * (8*p*(r.val+1)*(max 1 (v-1))^2*T+max 1 (v-1)+2)^
        ((r.val+1)*(r.val+2)/2))) ≤
      p*(M+1)^p * (capacityCoefficient p*(v+T+1)^(capacityDegree p)) := by
  calc
    _ ≤ ∑ r : Fin p, M.choose (r.val+1)*uniformCapacity p v T := by
      apply Finset.sum_le_sum
      intro r _
      apply Nat.mul_le_mul_left
      simpa [Nat.add_assoc] using uniformCapacity_bound (v := v) (T := T)
        (show r.val+1 ≤ p by omega)
    _ = (∑ r : Fin p, M.choose (r.val+1))*uniformCapacity p v T :=
      (Finset.sum_mul _ _ _).symm
    _ ≤ _ := Nat.mul_le_mul (chooseSum_bound M p) (uniformCapacity_polynomial p v T)

end CoverSizePolynomial
end DAGSpectral
