import Formal.DAGSpectral.Pseudoinverse
import Formal.DAGSpectral.CharpolyBits
import Formal.DAGSpectral.RatMatrix
import Mathlib.Algebra.Polynomial.Div

namespace DAGSpectral
open Matrix Polynomial Unitary

/-- Remove precisely the zero root factors, using exact rational coefficients. -/
noncomputable def zeroStripped (p : ℚ[X]) : ℚ[X] := p /ₘ X ^ p.natTrailingDegree

/-- On every nonzero root of p, this polynomial evaluates to its reciprocal. -/
noncomputable def reciprocalPolynomial (p : ℚ[X]) : ℚ[X] :=
  C (-(zeroStripped p).coeff 0)⁻¹ * (zeroStripped p).divX

theorem zeroStripped_factor (p : ℚ[X]) : X ^ p.natTrailingDegree * zeroStripped p = p := by
  simpa only [C_0, sub_zero, rootMultiplicity_eq_natTrailingDegree', zeroStripped] using
    p.pow_mul_divByMonic_rootMultiplicity_eq 0

theorem zeroStripped_constant_ne_zero {p : ℚ[X]} (hp : p ≠ 0) :
    (zeroStripped p).coeff 0 ≠ 0 := by
  simpa only [C_0, sub_zero, rootMultiplicity_eq_natTrailingDegree', zeroStripped,
    coeff_zero_eq_eval_zero] using p.eval_divByMonic_pow_rootMultiplicity_ne_zero 0 hp

theorem reciprocalPolynomial_on_root {p : ℚ[X]} (hp : p ≠ 0) {x : ℝ}
    (hx : x ≠ 0) (hroot : p.eval₂ (algebraMap ℚ ℝ) x = 0) :
    (reciprocalPolynomial p).eval₂ (algebraMap ℚ ℝ) x = x⁻¹ := by
  have hf := congrArg (fun q : ℚ[X] => q.eval₂ (algebraMap ℚ ℝ) x) (zeroStripped_factor p)
  simp only [eval₂_mul, eval₂_pow, eval₂_X, hroot] at hf
  have hz : (zeroStripped p).eval₂ (algebraMap ℚ ℝ) x = 0 :=
    (mul_eq_zero.mp hf).resolve_left (pow_ne_zero _ hx)
  have hd := congrArg (fun q : ℚ[X] => q.eval₂ (algebraMap ℚ ℝ) x)
    (zeroStripped p).X_mul_divX_add
  simp only [eval₂_add, eval₂_mul, eval₂_X, eval₂_C, hz] at hd
  have hc : ((zeroStripped p).coeff 0 : ℝ) ≠ 0 := by
    exact_mod_cast zeroStripped_constant_ne_zero hp
  simp only [reciprocalPolynomial, eval₂_mul, eval₂_C, map_inv₀, map_neg]
  change (-((zeroStripped p).coeff 0 : ℝ))⁻¹ * _ = x⁻¹
  change x * _ + ((zeroStripped p).coeff 0 : ℝ) = 0 at hd
  field_simp
  nlinarith

/-- All operations are finite rational polynomial and matrix arithmetic. -/
noncomputable def polynomialPseudoInverse {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    Matrix (Fin n) (Fin n) ℚ :=
  let R := aeval A (reciprocalPolynomial A.charpoly)
  A * R * R

theorem aeval_diagonal_rat {n : ℕ} (f : ℚ[X]) (v : Fin n → ℝ) :
    aeval (diagonal v) f = diagonal (fun i => f.eval₂ (algebraMap ℚ ℝ) (v i)) := by
  rw [show diagonal v = (Matrix.diagonalAlgHom ℚ) v from rfl,
    aeval_algHom_apply]
  change diagonal (aeval v f) = diagonal _
  apply congrArg diagonal
  funext i
  exact (aeval_algHom_apply (Pi.evalAlgHom ℚ (fun _ : Fin n => ℝ) i) v f).symm

theorem aeval_spectral_rat {n : ℕ} {A : RealMatrix n} (hA : A.IsHermitian) (f : ℚ[X]) :
    aeval A f = conjStarAlgAut ℚ _ hA.eigenvectorUnitary
      (diagonal fun i => f.eval₂ (algebraMap ℚ ℝ) (hA.eigenvalues i)) := by
  conv_lhs => arg 1; rw [spectral_real hA]
  change aeval ((conjStarAlgAut ℚ _ hA.eigenvectorUnitary)
    (diagonal hA.eigenvalues)) f = _
  rw [aeval_algHom_apply, aeval_diagonal_rat]

theorem ratMatrixReal_aeval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (f : ℚ[X]) :
    ratMatrixReal (aeval A f) = aeval (ratMatrixReal A) f := by
  exact (aeval_algHom_apply (Algebra.ofId ℚ ℝ).mapMatrix A f).symm

theorem rat_charpoly_eigen_root {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).IsHermitian) (i : Fin n) :
    A.charpoly.eval₂ (algebraMap ℚ ℝ) (hA.eigenvalues i) = 0 := by
  have hc : (A.charpoly.map (algebraMap ℚ ℝ)) = (ratMatrixReal A).charpoly := by
    exact (Matrix.charpoly_map A (algebraMap ℚ ℝ)).symm
  rw [← eval_map, hc, hA.charpoly_eq, eval_prod]
  apply Finset.prod_eq_zero (Finset.mem_univ i)
  simp

theorem polynomialPseudoInverse_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).IsHermitian) :
    ratMatrixReal (polynomialPseudoInverse A) = pseudoInverse (ratMatrixReal A) hA := by
  rw [polynomialPseudoInverse, ratMatrixReal_mul, ratMatrixReal_mul, ratMatrixReal_aeval]
  rw [aeval_spectral_rat hA]
  conv_lhs => lhs; lhs; rw [spectral_real hA]
  unfold pseudoInverse
  change conjStarAlgAut ℚ _ hA.eigenvectorUnitary (diagonal hA.eigenvalues) *
      conjStarAlgAut ℚ _ hA.eigenvectorUnitary
        (diagonal fun i => (reciprocalPolynomial A.charpoly).eval₂ (algebraMap ℚ ℝ)
          (hA.eigenvalues i)) *
      conjStarAlgAut ℚ _ hA.eigenvectorUnitary
        (diagonal fun i => (reciprocalPolynomial A.charpoly).eval₂ (algebraMap ℚ ℝ)
          (hA.eigenvalues i)) = _
  rw [← map_mul, ← map_mul, diagonal_mul_diagonal, diagonal_mul_diagonal]
  change (conjStarAlgAut ℚ _ hA.eigenvectorUnitary) _ =
    (conjStarAlgAut ℚ _ hA.eigenvectorUnitary) (diagonal fun i => (hA.eigenvalues i)⁻¹)
  apply congrArg (conjStarAlgAut ℚ _ hA.eigenvectorUnitary)
  apply congrArg diagonal
  funext i
  by_cases hi : hA.eigenvalues i = 0
  · simp [hi]
  · rw [reciprocalPolynomial_on_root A.charpoly_monic.ne_zero hi (rat_charpoly_eigen_root A hA i)]
    simp [hi]

/-- The exact finite set of nonzero characteristic coefficients. -/
def nonzeroCoefficientIndices {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : Finset ℕ :=
  (Finset.range (n+1)).filter (fun k => rationalCharpolyCoeff A k ≠ 0)

theorem nonzeroCoefficientIndices_nonempty {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (nonzeroCoefficientIndices A).Nonempty := by
  refine ⟨n, ?_⟩
  simp only [nonzeroCoefficientIndices, Finset.mem_filter, Finset.mem_range]
  refine ⟨by omega, ?_⟩
  rw [rationalCharpolyCoeff_eq]
  have hh := A.charpoly_monic.coeff_natDegree
  simpa only [Matrix.charpoly_natDegree_eq_dim, Fintype.card_fin] using
    (show A.charpoly.coeff A.charpoly.natDegree ≠ 0 by rw [hh]; norm_num)

def zeroRootIndex {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ℕ :=
  (nonzeroCoefficientIndices A).min' (nonzeroCoefficientIndices_nonempty A)

theorem zeroRootIndex_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    zeroRootIndex A = A.charpoly.natTrailingDegree := by
  apply le_antisymm
  · apply Finset.min'_le
    simp only [nonzeroCoefficientIndices, Finset.mem_filter, Finset.mem_range,
      rationalCharpolyCoeff_eq]
    constructor
    · have hh := natTrailingDegree_le_natDegree A.charpoly
      simp only [Matrix.charpoly_natDegree_eq_dim, Fintype.card_fin] at hh
      omega
    · exact coeff_natTrailingDegree_ne_zero.mpr A.charpoly_monic.ne_zero
  · apply Finset.le_min'
    intro k hk
    exact natTrailingDegree_le_of_ne_zero
      (by simpa only [rationalCharpolyCoeff_eq] using (Finset.mem_filter.mp hk).2)

/-- A finite rational matrix sum; no polynomial evaluator is executed. -/
def reciprocalMatrix {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    Matrix (Fin n) (Fin n) ℚ :=
  let k := zeroRootIndex A
  (-(rationalCharpolyCoeff A k))⁻¹ •
    ∑ i : Fin (n+1), rationalCharpolyCoeff A (i.val+1+k) • A^i.val

/-- The executable rational Moore–Penrose inverse producer. -/
def rationalPseudoInverse {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    Matrix (Fin n) (Fin n) ℚ := A * reciprocalMatrix A * reciprocalMatrix A

theorem zeroStripped_coeff (p : ℚ[X]) (i : ℕ) :
    (zeroStripped p).coeff i = p.coeff (i+p.natTrailingDegree) := by
  have hh := congrArg (fun f : ℚ[X] => f.coeff (i+p.natTrailingDegree)) (zeroStripped_factor p)
  simpa only [coeff_X_pow_mul] using hh

theorem reciprocalPolynomial_degree {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (reciprocalPolynomial A.charpoly).natDegree ≤ n := by
  apply (natDegree_C_mul_le _ _).trans
  apply natDegree_divX_le.trans
  rw [zeroStripped, natDegree_divByMonic _ (monic_X_pow _),
    Matrix.charpoly_natDegree_eq_dim, Fintype.card_fin]
  omega

theorem reciprocalMatrix_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    reciprocalMatrix A = aeval A (reciprocalPolynomial A.charpoly) := by
  rw [aeval_def, eval₂_eq_sum_range' _ (n := n+1) (by have := reciprocalPolynomial_degree A; omega)]
  simp only [reciprocalPolynomial, coeff_C_mul, coeff_divX, zeroStripped_coeff,
    zero_add, map_mul]
  rw [← Fin.sum_univ_eq_sum_range]
  unfold reciprocalMatrix
  simp only [zeroRootIndex_eq, rationalCharpolyCoeff_eq]
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro i _
  simp only [Algebra.algebraMap_eq_smul_one, smul_mul_assoc, one_mul, smul_smul]

theorem rationalPseudoInverse_eq_polynomial {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    rationalPseudoInverse A = polynomialPseudoInverse A := by
  simp only [rationalPseudoInverse, polynomialPseudoInverse, reciprocalMatrix_eq]

theorem rationalPseudoInverse_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).IsHermitian) :
    ratMatrixReal (rationalPseudoInverse A) = pseudoInverse (ratMatrixReal A) hA := by
  rw [rationalPseudoInverse_eq_polynomial]
  exact polynomialPseudoInverse_eq A hA

/-- Exact rational estimability test, including singular information matrices. -/
def rationalEstimable {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) : Bool :=
  decide (A *ᵥ (rationalPseudoInverse A *ᵥ c) = c)

theorem rationalEstimable_iff {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).IsHermitian) (c : Fin n → ℚ) :
    rationalEstimable A c = true ↔ Estimable (ratMatrixReal A) (fun i => (c i : ℝ)) := by
  rw [rationalEstimable, decide_eq_true_eq]
  have hh : (ratMatrixReal A) *ᵥ
      (pseudoInverse (ratMatrixReal A) hA *ᵥ (fun i => (c i : ℝ))) =
      fun i => ((A *ᵥ (rationalPseudoInverse A *ᵥ c)) i : ℝ) := by
    rw [← rationalPseudoInverse_eq A hA, ratMatrixReal_mulVec, ratMatrixReal_mulVec]
  constructor
  · intro hc
    refine ⟨pseudoInverse (ratMatrixReal A) hA *ᵥ (fun i => (c i : ℝ)), ?_⟩
    rw [hh, hc]
  · intro hc
    have he := pseudoInverse_solves hA hc
    rw [hh] at he
    funext i
    exact_mod_cast congrFun he i

/-- Rational evaluation of the quadratic Moore–Penrose form. -/
def rationalContrastVariance {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) : ℚ :=
  c ⬝ᵥ (rationalPseudoInverse A *ᵥ c)

theorem rationalContrastVariance_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).IsHermitian) (c : Fin n → ℚ) :
    (rationalContrastVariance A c : ℝ) =
      contrastVariance (ratMatrixReal A) hA (fun i => (c i : ℝ)) := by
  unfold contrastVariance rationalContrastVariance
  rw [← rationalPseudoInverse_eq A hA, ratMatrixReal_mulVec]
  simp [dotProduct]

end DAGSpectral
