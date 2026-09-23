import Formal.DAGSpectral.CoverNormalizationExecution

/-! Storage and container-control work recorded by the executed normalization caches.
Arithmetic trace allocation is instrumentation and is not charged here. -/
namespace DAGSpectral.CoverNormalizationExecution
open Matrix ReciprocalAnchor NormalizationBits
open scoped BigOperators

/-- Two materializations (results and rows), including vector loop control. -/
def matrixStorageBudget (l m B : ℕ) : ℕ := 2*(l*m*(2*B+1))+2*(l+1)*(m+1)

@[simp] theorem runMatrix_copies {l m : ℕ} (E : Fin l → Fin m → ArithmeticExpr) :
    (runMatrix E).copies = 2*RationalStorage.matrixCopy (fun i j => (E i j).eval) +
      2*(l+1)*(m+1) := by
  simp [runMatrix, RationalStorage.matrixCopy, RationalStorage.vectorCopy,
    ArithmeticExpr.run_eq]

theorem runMatrix_copies_le {l m B : ℕ} {E : Fin l → Fin m → ArithmeticExpr}
    (h : MatrixBits (fun i j => (E i j).eval) B) :
    (runMatrix E).copies ≤ matrixStorageBudget l m B := by
  rw [runMatrix_copies]
  exact Nat.add_le_add_right (Nat.mul_le_mul_left 2 (RationalStorage.matrixCopy_le h)) _

theorem mulRun_copies_le {l n m B : ℕ} {A : Matrix (Fin l) (Fin n) ℚ}
    {C : Matrix (Fin n) (Fin m) ℚ} (h : MatrixBits (A * C) B) :
    (mulRun A C).copies ≤ matrixStorageBudget l m B := by
  apply runMatrix_copies_le
  simpa only [matrixMulEntryExpr_eval] using h

theorem inverseRun_copies_le {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (h : MatrixBits (rationalMatrixInverse A) B) :
    (inverseRun A).copies ≤ matrixStorageBudget n n B := by
  apply runMatrix_copies_le
  simpa only [inverseEntryExpr_eval] using h

def normalizationStorageBudget (p r B T Q : ℕ) : ℕ :=
  matrixStorageBudget r r (gramBudget p B) +
  matrixStorageBudget r r (inverseBits r (gramBudget p B)) +
  matrixStorageBudget r p (leftBudget p r B) +
  matrixStorageBudget p p (projectorBudget p r B) +
  matrixStorageBudget r p (normalizerBudget p r B T) + r*(2*T+1)+(r+1) +
  matrixStorageBudget p r (restoreBudget r B T) +
  matrixStorageBudget r p (mulBudget p (normalizerBudget p r B T) Q) +
  matrixStorageBudget r r (transformBudget p r B T Q) + 1

theorem normalizeRun_copies_le {p r B T Q : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {τ : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T) (hA : MatrixBits A Q) :
    (normalizeRun V τ A).copies ≤ normalizationStorageBudget p r B T Q := by
  have hg := mulRun_copies_le (gram_bits hV)
  have hi := inverseRun_copies_le (matrixBits_inverse (gram_bits hV))
  have hl := mulRun_copies_le (left_bits hV)
  have hp := mulRun_copies_le (projector_bits hV)
  have ht := mulRun_copies_le (normalizer_bits hV hτ)
  have hk := mulRun_copies_le (restore_bits hV hτ)
  have hta := mulRun_copies_le (matrixBits_mul (normalizer_bits hV hτ) hA)
  have hata := mulRun_copies_le (transform_bits hV hτ hA)
  have hv := RationalStorage.vectorCopy_le (fun i => rationalBits_inv (hτ i))
  simp only [normalizeRun, mulRun_value, inverseRun_value, ArithmeticExpr.run_eq,
    ArithmeticExpr.eval, primitiveResult, Vector.get_ofFn] 
  dsimp only [normalizationStorageBudget]
  dsimp only [gramLeftInverseProducer, rangeProjectorProducer, normalizerProducer,
    reconstructorProducer, transformProducer] at hl hp ht hk hta hata
  dsimp only [mulBudget] at *
  omega

def atomStorageBudget (p r B T Q : ℕ) : ℕ := normalizationStorageBudget p r B T Q +
  matrixStorageBudget p p (mulBudget p (projectorBudget p r B) Q)+4*p*p+2*r+3

theorem atomRun_copies_le {p r B T Q : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {τ : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T) (hA : MatrixBits A Q) :
    (atomRun V τ A).copies ≤ atomStorageBudget p r B T Q := by
  have hn := normalizeRun_copies_le hV hτ hA
  have hp := mulRun_copies_le (matrixBits_mul (projector_bits hV) hA)
  simp only [atomRun, normalizeRun_projector]
  unfold atomStorageBudget mulBudget
  omega

def labelStorageBudget (r B C : ℕ) : ℕ :=
  matrixStorageBudget r r (B+C)+r*r*(B+C+2)+(r+1)*(r+1)

theorem labelRun_copies_le {r B C : ℕ} {A : Matrix (Fin r) (Fin r) ℚ} {h : ℚ}
    (hA : MatrixBits A B) (hh : RationalBits h C) :
    (labelRun A h).copies ≤ labelStorageBudget r B C := by
  have hq : MatrixBits (fun i j => A i j / h) (B+C) :=
    fun i j => rationalBits_div (hA i j) hh
  have hc := runMatrix_copies_le (E := fun i j => .op .div (.atom (A i j)) (.atom h)) hq
  have hf : (∑ i, ∑ j, ((⌊A i j/h⌋:ℤ).natAbs.size+1)) ≤ r*r*(B+C+2) := by
    have hh := Finset.sum_le_sum (s := Finset.univ) fun i _ =>
      Finset.sum_le_sum (s := Finset.univ) fun j _ =>
        Nat.add_le_add_right (Nat.size_le.mpr (integerBits_floor (hq i j))) 1
    simpa [Nat.mul_assoc, Nat.add_assoc] using hh
  simp only [labelRun, Vector.get_ofFn]
  change (runMatrix _).copies +
    (∑ i, ∑ j, ((⌊(runMatrix
      (fun i j => .op .div (.atom (A i j)) (.atom h))).value i j⌋:ℤ).natAbs.size+1)) + _ ≤ _
  simp only [runMatrix_value, ArithmeticExpr.eval, primitiveResult]
  unfold labelStorageBudget
  omega

def trialStorageBudget (p r m B T Q C : ℕ) : ℕ :=
  (m+1)*atomStorageBudget p r B T Q +
    m*labelStorageBudget r (transformBudget p r B T Q) C + 2*(m+1)+1

theorem trialRun_copies_le {p r m B T Q C : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {τ : Fin r → ℚ} {A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ} {h : ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T)
    (hA : ∀ e, MatrixBits (A e) Q) (hh : RationalBits h C) :
    (trialRun V τ A h).copies ≤ trialStorageBudget p r m B T Q C := by
  have hp := atomRun_copies_le hV hτ (hA none)
  have ha := Finset.sum_le_sum (s := Finset.univ) fun e _ => atomRun_copies_le hV hτ (hA (some e))
  have hl := Finset.sum_le_sum (s := Finset.univ) fun e _ =>
    labelRun_copies_le (transform_bits hV hτ (hA (some e))) hh
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at ha hl
  simp only [trialRun, Vector.get_ofFn, atomRun_normalized, normalizeRun_atom]
  unfold trialStorageBudget
  nlinarith

theorem matrixStorageBudget_scale {l m B C K : ℕ} (hB : B ≤ C * K) (hK : 1 ≤ K) :
    matrixStorageBudget l m B ≤ matrixStorageBudget l m C * K := by
  have h : 2*B+1 ≤ (2*C+1)*K := by nlinarith only [hB, hK]
  have hh := Nat.mul_le_mul_left (2*(l*m)) h
  have hc := Nat.mul_le_mul_left (2*(l+1)*(m+1)) hK
  unfold matrixStorageBudget
  nlinarith only [hh, hc]

theorem normalizationStorageBudget_scale {p r B T Q b t q K : ℕ}
    (hB : B ≤ b * K) (hT : T ≤ t * K) (hQ : Q ≤ q * K) (hK : 1 ≤ K) :
    normalizationStorageBudget p r B T Q ≤ normalizationStorageBudget p r b t q * K := by
  have h1 := matrixStorageBudget_scale (l := r) (m := r) (gramBudget_scale (p := p) hB hK) hK
  have h2 := matrixStorageBudget_scale (l := r) (m := r)
    (inverseBits_scale (n := r) (gramBudget_scale (p := p) hB hK) hK) hK
  have h3 := matrixStorageBudget_scale (l := r) (m := p) 
    (leftBudget_scale (p := p) (r := r) hB hK) hK
  have h4 := matrixStorageBudget_scale (l := p) (m := p) 
    (projectorBudget_scale (p := p) (r := r) hB hK) hK
  have h5 := matrixStorageBudget_scale (l := r) (m := p) 
    (normalizerBudget_scale (p := p) (r := r) hB hT hK) hK
  have h6 := matrixStorageBudget_scale (l := p) (m := r) (restoreBudget_scale (r := r) hB hT hK) hK
  have h7 := matrixStorageBudget_scale (l := r) (m := p)
    (mulBudget_scale (n := p) (normalizerBudget_scale (p := p) (r := r) hB hT hK) hQ hK) hK
  have h8 := matrixStorageBudget_scale (l := r) (m := r) 
    (transformBudget_scale (p := p) (r := r) hB hT hQ hK) hK
  have hv : r*(2*T+1) ≤ r*(2*t+1)*K := by
    have h : 2*T+1 ≤ (2*t+1)*K := by nlinarith only [hT, hK]
    exact (Nat.mul_le_mul_left r h).trans_eq (by ring)
  have hc := Nat.mul_le_mul_left (r+2) hK
  unfold normalizationStorageBudget
  nlinarith only [h1,h2,h3,h4,h5,h6,h7,h8,hv,hc]

theorem atomStorageBudget_scale {p r B T Q b t q K : ℕ}
    (hB : B ≤ b * K) (hT : T ≤ t * K) (hQ : Q ≤ q * K) (hK : 1 ≤ K) :
    atomStorageBudget p r B T Q ≤ atomStorageBudget p r b t q * K := by
  have hn := normalizationStorageBudget_scale (p := p) (r := r) hB hT hQ hK
  have hm := matrixStorageBudget_scale (l := p) (m := p)
    (mulBudget_scale (n := p) (projectorBudget_scale (p := p) (r := r) hB hK) hQ hK) hK
  have hc := Nat.mul_le_mul_left (4*p*p+2*r+3) hK
  unfold atomStorageBudget
  nlinarith only [hn, hm, hc]

theorem labelStorageBudget_scale {r B C b c K : ℕ}
    (hB : B ≤ b * K) (hC : C ≤ c * K) (hK : 1 ≤ K) :
    labelStorageBudget r B C ≤ labelStorageBudget r b c * K := by
  have hm := matrixStorageBudget_scale (l := r) (m := r)
    (show B+C ≤ (b+c)*K by nlinarith only [hB,hC]) hK
  have hl := Nat.mul_le_mul_left (r*r) (show B+C+2 ≤ (b+c+2)*K by nlinarith only [hB,hC,hK])
  have hc := Nat.mul_le_mul_left ((r+1)*(r+1)) hK
  unfold labelStorageBudget
  nlinarith only [hm,hl,hc]

theorem trialStorageBudget_scale {p r m B T Q C b t q c K : ℕ}
    (hB : B ≤ b * K) (hT : T ≤ t * K) (hQ : Q ≤ q * K) (hC : C ≤ c * K) (hK : 1 ≤ K) :
    trialStorageBudget p r m B T Q C ≤ trialStorageBudget p r m b t q c * K := by
  have ha := Nat.mul_le_mul_left (m+1) (atomStorageBudget_scale (p := p) (r := r) hB hT hQ hK)
  have hl := Nat.mul_le_mul_left m (labelStorageBudget_scale (r := r)
    (transformBudget_scale (p := p) (r := r) hB hT hQ hK) hC hK)
  have hc := Nat.mul_le_mul_left (2*(m+1)+1) hK
  unfold trialStorageBudget
  nlinarith only [ha,hl,hc]

end DAGSpectral.CoverNormalizationExecution
