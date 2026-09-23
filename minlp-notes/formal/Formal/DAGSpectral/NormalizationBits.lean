import Formal.DAGSpectral.NormalizationProducer
import Formal.DAGSpectral.DyadicScaleBits
import Formal.DAGSpectral.NormalizationTrials
import Formal.DAGSpectral.MatrixArithmeticTrace

/-! Rational entry bounds for the executable normalization. The budgets are
explicit affine functions of the input bit bounds at every fixed pair of dimensions. -/
namespace DAGSpectral
open Matrix ReciprocalAnchor

namespace NormalizationBits

/-- A matrix multiplication with this inner dimension has this entry budget. -/
def mulBudget (n B C : ℕ) : ℕ := 1+n*(B+C+1)
def gramBudget (p B : ℕ) : ℕ := mulBudget p B B
def leftBudget (p r B : ℕ) : ℕ := mulBudget r (inverseBits r (gramBudget p B)) B
def projectorBudget (p r B : ℕ) : ℕ := mulBudget r B (leftBudget p r B)
def normalizerBudget (p r B T : ℕ) : ℕ := mulBudget r (T+1) (leftBudget p r B)
def restoreBudget (r B T : ℕ) : ℕ := mulBudget r B (T+1)
def transformBudget (p r B T Q : ℕ) : ℕ :=
  mulBudget p (mulBudget p (normalizerBudget p r B T) Q) (normalizerBudget p r B T)

theorem matrixBits_mono {ι κ : Type*} {A : Matrix ι κ ℚ} {B C : ℕ}
    (hA : MatrixBits A B) (hBC : B ≤ C) : MatrixBits A C :=
  fun i j => rationalBits_mono (hA i j) hBC

theorem diagonal_bits {r T : ℕ} {τ : Fin r → ℚ}
    (hτ : ∀ i, RationalBits (τ i) T) : MatrixBits (diagonal τ) (T+1) := by
  intro i j
  simp only [Matrix.diagonal_apply]
  split_ifs
  · exact rationalBits_mono (hτ _) (by omega)
  · exact rationalBits_mono rationalBits_zero (by omega)

theorem gram_bits {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    (hV : MatrixBits V B) : MatrixBits (Vᵀ*V) (gramBudget p B) :=
  matrixBits_mul (matrixBits_transpose hV) hV

theorem left_bits {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    (hV : MatrixBits V B) : MatrixBits (gramLeftInverseProducer V) (leftBudget p r B) :=
  matrixBits_mul (matrixBits_inverse (gram_bits hV)) (matrixBits_transpose hV)

theorem projector_bits {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    (hV : MatrixBits V B) : MatrixBits (rangeProjectorProducer V) (projectorBudget p r B) :=
  matrixBits_mul hV (left_bits hV)

theorem normalizer_bits {p r B T : ℕ} {V : Matrix (Fin p) (Fin r) ℚ} {τ : Fin r → ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T) :
    MatrixBits (normalizerProducer V τ) (normalizerBudget p r B T) :=
  matrixBits_mul (diagonal_bits hτ) (left_bits hV)

theorem restore_bits {p r B T : ℕ} {V : Matrix (Fin p) (Fin r) ℚ} {τ : Fin r → ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T) :
    MatrixBits (reconstructorProducer V τ) (restoreBudget r B T) :=
  matrixBits_mul hV (diagonal_bits (fun i => rationalBits_inv (hτ i)))

theorem transform_bits {p r B T Q : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {τ : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T) (hA : MatrixBits A Q) :
    MatrixBits (transformProducer V τ A) (transformBudget p r B T Q) :=
  matrixBits_mul (matrixBits_mul (normalizer_bits hV hτ) hA)
    (matrixBits_transpose (normalizer_bits hV hτ))

/-- Exact denominator/numerator lengths are used by the actual normalization trials. -/
abbrev actualWeightBits (w : ℚ) : ℕ := NormalizationTrials.weightBits w

theorem actualWeightBits_le {w : ℚ} {B : ℕ} (hw : RationalBits w B) : actualWeightBits w ≤ B := by
  obtain ⟨hn,hd⟩ := (rationalBits_iff_size w B).mp hw
  exact max_le hn hd

theorem actualWeightBits_spec (w : ℚ) : RationalBits w (actualWeightBits w) := by
  rw [rationalBits_iff_size]
  exact ⟨le_max_left _ _,le_max_right _ _⟩

def actualScales {r : ℕ} (w : Fin r → ℚ) : Fin r → ℚ :=
  fun j => dyadicScale (w j) (actualWeightBits (w j))

theorem actualScales_bits {r B : ℕ} {w : Fin r → ℚ}
    (hw : ∀ i, RationalBits (w i) B) : ∀ i, RationalBits (actualScales w i) (6*B+1) := by
  intro i
  exact rationalBits_mono (dyadicScale_bits _ _) (by have := actualWeightBits_le (hw i); omega)

/-- All dyadic searches, using their actual input sizes rather than a supplied bound. -/
def scalesTrace {r : ℕ} (w : Fin r → ℚ) : List ArithmeticEvent :=
  (List.ofFn fun i => dyadicScaleTrace (w i) (actualWeightBits (w i))).flatten

theorem scalesTrace_length {r B : ℕ} {w : Fin r → ℚ}
    (hw : ∀ i, RationalBits (w i) B) : (scalesTrace w).length ≤ r*(9*B+1) := by
  simp only [scalesTrace,List.length_flatten,List.map_ofFn,List.sum_ofFn]
  calc
    _ ≤ ∑ _i : Fin r, (9*B+1) := by
      apply Finset.sum_le_sum
      intro i _
      exact (dyadicScaleTrace_length _ _).trans (by have := actualWeightBits_le (hw i); omega)
    _ = _ := by simp

theorem scalesTrace_bits {r B : ℕ} {w : Fin r → ℚ}
    (hw : ∀ i, RationalBits (w i) B) : ∀ e ∈ scalesTrace w, eventBits (13*B+4) e := by
  intro e he
  obtain ⟨xs,hxs,he⟩ := List.mem_flatten.mp he
  obtain ⟨i,rfl⟩ := List.mem_ofFn.mp hxs
  have hh := dyadicScaleTrace_bits (actualWeightBits_spec (w i)) e he
  have hb : 13*actualWeightBits (w i)+4 ≤ 13*B+4 := by
    have := actualWeightBits_le (hw i)
    omega
  exact ⟨rationalBits_mono hh.1 hb,rationalBits_mono hh.2 hb⟩

private theorem add_one_scale {B C K : ℕ} (h : B ≤ C * K) (hK : 1 ≤ K) :
    B+1 ≤ (C+1) * K := by nlinarith

theorem mulBudget_scale {n B C D E K : ℕ} (hB : B ≤ D * K) (hC : C ≤ E * K)
    (hK : 1 ≤ K) : mulBudget n B C ≤ mulBudget n D E * K := by
  unfold mulBudget
  calc
    _ ≤ K+n*((D+E+1) * K) := Nat.add_le_add hK (Nat.mul_le_mul_left _ (by nlinarith))
    _ = _ := by ring

theorem determinantBits_scale {n B C K : ℕ} (hB : B ≤ C * K) (hK : 1 ≤ K) :
    determinantBits n B ≤ determinantBits n C * K := by
  unfold determinantBits
  calc
    _ ≤ K+n.factorial*((n*C+3) * K) := by
      apply Nat.add_le_add hK
      apply Nat.mul_le_mul_left
      nlinarith
    _ = _ := by ring

theorem inverseBits_scale {n B C K : ℕ} (hB : B ≤ C * K) (hK : 1 ≤ K) :
    inverseBits n B ≤ inverseBits n C * K := by
  have h := determinantBits_scale (n := n) (add_one_scale hB hK) hK
  unfold inverseBits
  nlinarith

theorem gramBudget_scale {p B C K : ℕ} (hB : B ≤ C * K) (hK : 1 ≤ K) :
    gramBudget p B ≤ gramBudget p C * K := mulBudget_scale hB hB hK

theorem leftBudget_scale {p r B C K : ℕ} (hB : B ≤ C * K) (hK : 1 ≤ K) :
    leftBudget p r B ≤ leftBudget p r C * K :=
  mulBudget_scale (inverseBits_scale (gramBudget_scale hB hK) hK) hB hK

theorem projectorBudget_scale {p r B C K : ℕ} (hB : B ≤ C * K) (hK : 1 ≤ K) :
    projectorBudget p r B ≤ projectorBudget p r C * K :=
  mulBudget_scale hB (leftBudget_scale hB hK) hK

theorem normalizerBudget_scale {p r B C T U K : ℕ}
    (hB : B ≤ C * K) (hT : T ≤ U * K) (hK : 1 ≤ K) :
    normalizerBudget p r B T ≤ normalizerBudget p r C U * K :=
  mulBudget_scale (add_one_scale hT hK) (leftBudget_scale hB hK) hK

theorem restoreBudget_scale {r B C T U K : ℕ}
    (hB : B ≤ C * K) (hT : T ≤ U * K) (hK : 1 ≤ K) :
    restoreBudget r B T ≤ restoreBudget r C U * K :=
  mulBudget_scale hB (add_one_scale hT hK) hK

theorem transformBudget_scale {p r B C T U Q R K : ℕ}
    (hB : B ≤ C * K) (hT : T ≤ U * K) (hQ : Q ≤ R * K) (hK : 1 ≤ K) :
    transformBudget p r B T Q ≤ transformBudget p r C U R * K :=
  mulBudget_scale (mulBudget_scale (normalizerBudget_scale hB hT hK) hQ hK)
    (normalizerBudget_scale hB hT hK) hK

/-- With fixed dimensions, actual dyadic normalization has linear coefficient-bit growth. -/
theorem dyadicTransformBudget_linear (p r B : ℕ) :
    transformBudget p r B (6*B+1) B ≤ transformBudget p r 1 7 1*(B+1) :=
  transformBudget_scale (by omega) (by omega) (by omega) (by omega)

/-- A common bound for every input to one matrix primitive in normalization. -/
def operandBudget (p r B T Q : ℕ) : ℕ :=
  B+(T+1)+Q+gramBudget p B+inverseBits r (gramBudget p B)+leftBudget p r B+
    projectorBudget p r B+normalizerBudget p r B T+restoreBudget r B T+
    mulBudget p (normalizerBudget p r B T) Q+transformBudget p r B T Q+1

theorem operandBudget_pos (p r B T Q : ℕ) : 0 < operandBudget p r B T Q := by
  unfold operandBudget
  omega

theorem operandBudget_scale {p r B C T U Q R K : ℕ}
    (hB : B ≤ C * K) (hT : T ≤ U * K) (hQ : Q ≤ R * K) (hK : 1 ≤ K) :
    operandBudget p r B T Q ≤ operandBudget p r C U R * K := by
  have hg := gramBudget_scale (p := p) hB hK
  have hi := inverseBits_scale (n := r) hg hK
  have hl := leftBudget_scale (p := p) (r := r) hB hK
  have hp := projectorBudget_scale (p := p) (r := r) hB hK
  have hn := normalizerBudget_scale (p := p) (r := r) hB hT hK
  have hr := restoreBudget_scale (r := r) hB hT hK
  have hm := mulBudget_scale (n := p) hn hQ hK
  have ht := transformBudget_scale (p := p) (r := r) hB hT hQ hK
  have hT' := add_one_scale hT hK
  unfold operandBudget
  nlinarith

theorem dyadicOperandBudget_linear (p r B : ℕ) :
    operandBudget p r B (6*B+1) B ≤ operandBudget p r 1 7 1*(B+1) :=
  operandBudget_scale (by omega) (by omega) (by omega) (by omega)

/-- Eager evaluation of each finite intermediate matrix once. Scalar traces
are executable expressions proved equal to the matrix formulas. -/
def normalizationTrace {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ)
    (A : Matrix (Fin p) (Fin p) ℚ) : List ArithmeticEvent :=
  matrixMulTrace Vᵀ V ++ matrixInverseTrace (Vᵀ*V) ++
    matrixMulTrace (rationalMatrixInverse (Vᵀ*V)) Vᵀ ++
    matrixMulTrace V (gramLeftInverseProducer V) ++
    matrixMulTrace (diagonal τ) (gramLeftInverseProducer V) ++
    List.ofFn (fun i => (ReciprocalAnchor.ManyLeaf.BitCost.RationalPrimitive.inv,τ i,0)) ++
    matrixMulTrace V (diagonal (fun i => (τ i)⁻¹)) ++
    matrixMulTrace (normalizerProducer V τ) A ++
    matrixMulTrace (normalizerProducer V τ*A) (normalizerProducer V τ)ᵀ

def normalizationOperations (p r : ℕ) : ℕ :=
  r*r*(2*p)+r*r*(2*determinantOperations r+2)+r*p*(2*r)+p*p*(2*r)+r*p*(2*r)+r+
    p*r*(2*r)+r*p*(2*p)+r*r*(2*p)

theorem normalizationTrace_length {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (normalizationTrace V τ A).length = normalizationOperations p r := by
  simp [normalizationTrace,normalizationOperations,add_assoc]

def normalizationDepth (p r : ℕ) : ℕ := 2*p+2*r+2*determinantOperations r+2

def traceBudget (p r B T Q : ℕ) : ℕ :=
  arithmeticWidth (normalizationDepth p r) (operandBudget p r B T Q)

theorem normalizationTrace_bits {p r B T Q : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {τ : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T) (hA : MatrixBits A Q) :
    ∀ e ∈ normalizationTrace V τ A, eventBits (traceBudget p r B T Q) e := by
  let C := operandBudget p r B T Q
  have hC : 0 < C := operandBudget_pos _ _ _ _ _
  have hv : MatrixBits V C := matrixBits_mono hV (by dsimp [C,operandBudget]; omega)
  have ha : MatrixBits A C := matrixBits_mono hA (by dsimp [C,operandBudget]; omega)
  have hg : MatrixBits (Vᵀ*V) C :=
    matrixBits_mono (gram_bits hV) (by dsimp [C,operandBudget]; omega)
  have hi : MatrixBits (rationalMatrixInverse (Vᵀ*V)) C :=
    matrixBits_mono (matrixBits_inverse (gram_bits hV)) (by dsimp [C,operandBudget]; omega)
  have hl : MatrixBits (gramLeftInverseProducer V) C :=
    matrixBits_mono (left_bits hV) (by dsimp [C,operandBudget]; omega)
  have hd : MatrixBits (diagonal τ) C :=
    matrixBits_mono (diagonal_bits hτ) (by dsimp [C,operandBudget]; omega)
  have hdi : MatrixBits (diagonal (fun i => (τ i)⁻¹)) C :=
    matrixBits_mono (diagonal_bits (fun i => rationalBits_inv (hτ i)))
      (by dsimp [C,operandBudget]; omega)
  have hn : MatrixBits (normalizerProducer V τ) C :=
    matrixBits_mono (normalizer_bits hV hτ) (by dsimp [C,operandBudget]; omega)
  have hm : MatrixBits (normalizerProducer V τ*A) C :=
    matrixBits_mono (matrixBits_mul (normalizer_bits hV hτ) hA)
      (by dsimp [C,operandBudget,mulBudget]; omega)
  have widen {d : ℕ} {e : ArithmeticEvent} (hd : d ≤ normalizationDepth p r)
      (he : eventBits (arithmeticWidth d C) e) : eventBits (traceBudget p r B T Q) e :=
    eventBits_mono he (arithmeticWidth_mono hd)
  intro e he
  simp only [normalizationTrace,List.mem_append] at he
  rcases he with (((((((he|he)|he)|he)|he)|he)|he)|he)|he
  · exact widen (by unfold normalizationDepth; omega)
      (matrixMulTrace_bits hC (matrixBits_transpose hv) hv e he)
  · exact widen (by unfold normalizationDepth; omega) (matrixInverseTrace_bits hC hg e he)
  · exact widen (by unfold normalizationDepth; omega)
      (matrixMulTrace_bits hC hi (matrixBits_transpose hv) e he)
  · exact widen (by unfold normalizationDepth; omega) (matrixMulTrace_bits hC hv hl e he)
  · exact widen (by unfold normalizationDepth; omega) (matrixMulTrace_bits hC hd hl e he)
  · obtain ⟨i,rfl⟩ := List.mem_ofFn.mp he
    have hw : eventBits C (ReciprocalAnchor.ManyLeaf.BitCost.RationalPrimitive.inv,τ i,0) :=
      ⟨rationalBits_mono (hτ i) (by dsimp [C,operandBudget]; omega),
       rationalBits_mono rationalBits_zero hC⟩
    exact widen (d := 0) (Nat.zero_le _) (by simpa [arithmeticWidth_zero] using hw)
  · exact widen (by unfold normalizationDepth; omega) (matrixMulTrace_bits hC hv hdi e he)
  · exact widen (by unfold normalizationDepth; omega) (matrixMulTrace_bits hC hn ha e he)
  · exact widen (by unfold normalizationDepth; omega)
      (matrixMulTrace_bits hC hm (matrixBits_transpose hn) e he)

theorem normalization_bitWork {p r B T Q : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {τ : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T) (hA : MatrixBits A Q) :
    traceBitWork (traceBudget p r B T Q) (normalizationTrace V τ A) ≤
      normalizationOperations p r*(256*(traceBudget p r B T Q+1)^3) := by
  simpa only [normalizationTrace_length] using traceBitWork_le (normalizationTrace_bits hV hτ hA)

/-- Dyadic-scale construction followed by the complete rational normalization. -/
def dyadicNormalizationTrace {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (w : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) : List ArithmeticEvent :=
  scalesTrace w ++ normalizationTrace V (actualScales w) A

def dyadicTraceBudget (p r B : ℕ) : ℕ := 13*B+4+traceBudget p r B (6*B+1) B

theorem dyadicNormalizationTrace_bits {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {w : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hw : ∀ i, RationalBits (w i) B) (hA : MatrixBits A B) :
    ∀ e ∈ dyadicNormalizationTrace V w A, eventBits (dyadicTraceBudget p r B) e := by
  intro e he
  rcases List.mem_append.mp he with he | he
  · exact eventBits_mono (scalesTrace_bits hw e he) (by unfold dyadicTraceBudget; omega)
  · exact eventBits_mono (normalizationTrace_bits hV (actualScales_bits hw) hA e he)
      (by unfold dyadicTraceBudget; omega)

theorem dyadicNormalizationTrace_length {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {w : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hw : ∀ i, RationalBits (w i) B) :
    (dyadicNormalizationTrace V w A).length ≤ r*(9*B+1)+normalizationOperations p r := by
  simp only [dyadicNormalizationTrace,List.length_append,normalizationTrace_length]
  exact Nat.add_le_add_right (scalesTrace_length hw) _

theorem dyadicNormalization_bitWork {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {w : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hw : ∀ i, RationalBits (w i) B) (hA : MatrixBits A B) :
    traceBitWork (dyadicTraceBudget p r B) (dyadicNormalizationTrace V w A) ≤
      (r*(9*B+1)+normalizationOperations p r)*(256*(dyadicTraceBudget p r B+1)^3) :=
  (traceBitWork_le (dyadicNormalizationTrace_bits hV hw hA)).trans
    (Nat.mul_le_mul_right _ (dyadicNormalizationTrace_length hw))

def normalizationBitCoefficient (p r : ℕ) : ℕ :=
  17+2^(normalizationDepth p r)*(operandBudget p r 1 7 1+2)

theorem dyadicTraceBudget_linear (p r B : ℕ) :
    dyadicTraceBudget p r B ≤ normalizationBitCoefficient p r*(B+1) := by
  have hc := dyadicOperandBudget_linear p r B
  have hh : operandBudget p r B (6*B+1) B+2 ≤
      (operandBudget p r 1 7 1+2)*(B+1) := by nlinarith
  unfold dyadicTraceBudget traceBudget arithmeticWidth normalizationBitCoefficient
  calc
    _ ≤ 13*B+4+2^(normalizationDepth p r)*
        (operandBudget p r B (6*B+1) B+2) := Nat.add_le_add_left (Nat.sub_le _ _) _
    _ ≤ 17*(B+1)+2^(normalizationDepth p r)*
        ((operandBudget p r 1 7 1+2)*(B+1)) :=
      Nat.add_le_add (by omega) (Nat.mul_le_mul_left _ hh)
    _ = _ := by ring

def normalizationCostCoefficient (p r : ℕ) : ℕ :=
  (10*r+normalizationOperations p r)*256*(normalizationBitCoefficient p r+1)^3

/-- A degree-four polynomial in the rational input bit bound, at fixed dimensions.
The model includes the actual numerator-size dyadic searches and all scalar
matrix operations, including determinant/adjugate inverse evaluation. -/
theorem dyadicNormalization_bitWork_polynomial {p r B : ℕ}
    {V : Matrix (Fin p) (Fin r) ℚ} {w : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hw : ∀ i, RationalBits (w i) B) (hA : MatrixBits A B) :
    traceBitWork (dyadicTraceBudget p r B) (dyadicNormalizationTrace V w A) ≤
      normalizationCostCoefficient p r*(B+1)^4 := by
  have hc : r*(9*B+1)+normalizationOperations p r ≤
      (10*r+normalizationOperations p r)*(B+1) := by nlinarith
  have hb : dyadicTraceBudget p r B+1 ≤
      (normalizationBitCoefficient p r+1)*(B+1) := by
    have := dyadicTraceBudget_linear p r B
    nlinarith
  apply (dyadicNormalization_bitWork hV hw hA).trans
  calc
    _ ≤ ((10*r+normalizationOperations p r)*(B+1))*
        (256*((normalizationBitCoefficient p r+1)*(B+1))^3) :=
      Nat.mul_le_mul hc (Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hb 3))
    _ = _ := by unfold normalizationCostCoefficient; ring

end NormalizationBits
end DAGSpectral
