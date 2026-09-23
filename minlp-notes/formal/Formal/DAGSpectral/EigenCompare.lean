import Formal.DAGSpectral.EigenCompareDifference
import Formal.DAGSpectral.EigenComparePSD
import Formal.DAGSpectral.EigenCompareBisection
import Formal.DAGSpectral.CharpolyBits

/-! Exact rational threshold tests and finite dyadic comparison of least
 eigenvalues. Every comparison is performed on rational data. -/
namespace DAGSpectral
open Matrix
open scoped MatrixOrder

/-- A finite rational coefficient test; it never compares real eigenvalues. -/
def rationalPSDTest {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : Bool :=
  (List.range (n+1)).all (fun k => decide (0 ≤ rationalCharpolyCoeff (-A) k))

theorem rationalPSDTest_correct {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).IsHermitian) :
    rationalPSDTest A = true ↔ (ratMatrixReal A).PosSemidef := by
  rw [posSemidef_iff_charpoly_neg_coeff_nonneg hA]
  have hcoeff (k : ℕ) : ((rationalCharpolyCoeff (-A) k : ℚ) : ℝ) =
      (-ratMatrixReal A).charpoly.coeff k := by
    rw [rationalCharpolyCoeff_eq]
    have he : -ratMatrixReal A = ratMatrixReal (-A) := by ext i j; simp
    rw [he]
    rw [ratMatrixReal, Matrix.charpoly_map, Polynomial.coeff_map]
    rfl
  simp only [rationalPSDTest, List.all_eq_true, List.mem_range, decide_eq_true_eq]
  constructor
  · intro h k
    by_cases hk : k < n+1
    · rw [← hcoeff]
      exact_mod_cast h k hk
    · have hz : (-ratMatrixReal A).charpoly.coeff k = 0 :=
        Polynomial.coeff_eq_zero_of_natDegree_lt (by
          simp only [Matrix.charpoly_natDegree_eq_dim, Fintype.card_fin]
          omega)
      rw [hz]
  · intro h k _
    have hh := h k
    rw [← hcoeff] at hh
    exact_mod_cast hh

def eigenThresholdTest {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (q : ℚ) : Bool :=
  rationalPSDTest (A - q • 1)

theorem eigenThresholdTest_correct {n : ℕ} [Nonempty (Fin n)]
    (A : Matrix (Fin n) (Fin n) ℚ) (hA : (ratMatrixReal A).IsHermitian) (q : ℚ) :
    eigenThresholdTest A q = true ↔ (q : ℝ) ≤ minimumEigenvalue (ratMatrixReal A) := by
  have he : ratMatrixReal (A - q • 1) = ratMatrixReal A - (q : ℝ) • 1 := by
    ext i j
    simp only [ratMatrixReal_apply, Matrix.sub_apply, Matrix.smul_apply,
      smul_eq_mul, Matrix.one_apply]
    split_ifs <;> push_cast <;> ring
  have hh : (ratMatrixReal (A - q • 1)).IsHermitian := by
    rw [he]
    exact hA.sub (isHermitian_one.smul (by simp))
  rw [eigenThresholdTest, rationalPSDTest_correct _ hh, he,
    minimumEigenvalue_of_hermitian hA,
    scalar_le_hermitianMinimum_iff]
  rfl

def eigenSearchRadius {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) : ℚ :=
  1 + ∑ i, |A i i| + ∑ i, |B i i|

theorem eigenSearchRadius_pos {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    0 < eigenSearchRadius A B := by
  unfold eigenSearchRadius
  positivity

theorem minimumEigenvalue_le_diag {ι : Type*} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    {A : Matrix ι ι ℝ} (hA : A.IsHermitian) (i : ι) :
    minimumEigenvalue A ≤ A i i := by
  have hs := (scalar_le_hermitianMinimum_iff hA (hermitianMinimum hA)).mp le_rfl
  have hd := (Matrix.le_iff.mp hs).diag_nonneg (i := i)
  simpa [minimumEigenvalue_of_hermitian hA] using hd

theorem minimumEigenvalue_le_radius {n : ℕ} [Nonempty (Fin n)]
    (A B : Matrix (Fin n) (Fin n) ℚ) (hA : (ratMatrixReal A).IsHermitian) :
    minimumEigenvalue (ratMatrixReal A) ≤ (eigenSearchRadius A B : ℝ) := by
  classical
  let i : Fin n := Classical.choice inferInstance
  have hh := minimumEigenvalue_le_diag hA i
  have hi := Finset.single_le_sum (fun j (_ : j ∈ Finset.univ) => abs_nonneg (A j j))
    (Finset.mem_univ i)
  have hi' : |(A i i : ℝ)| ≤ ∑ j, |(A j j : ℝ)| := by exact_mod_cast hi
  have hs : (0 : ℝ) ≤ ∑ j, |(B j j : ℝ)| := Finset.sum_nonneg (fun _ _ => abs_nonneg _)
  simp only [ratMatrixReal_apply] at hh
  unfold eigenSearchRadius
  push_cast
  linarith [le_abs_self (A i i : ℝ)]

def eigenDifferenceFinite {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    Matrix (Fin (n*n)) (Fin (n*n)) ℚ :=
  Matrix.reindex finProdFinEquiv finProdFinEquiv (eigenDifferenceMatrix A B)

def eigenDifferenceCoefficients {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) : List ℚ :=
  List.ofFn (fun i : Fin (n*n+1) => rationalCharpolyCoeff (eigenDifferenceFinite A B) i)

def eigenComparisonGap {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) : ℚ :=
  separationFromCoefficients (eigenDifferenceCoefficients A B)

theorem eigenComparisonGap_eq {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    eigenComparisonGap A B = ratRootSeparation (eigenDifferencePolynomial A B) := by
  have he (i : Fin (n*n+1)) : rationalCharpolyCoeff (eigenDifferenceFinite A B) i =
      (eigenDifferencePolynomial A B).coeff i := by
    rw [rationalCharpolyCoeff_eq, eigenDifferenceFinite, Matrix.charpoly_reindex]
    rfl
  simp only [eigenComparisonGap, eigenDifferenceCoefficients, he]
  exact separationFromCoefficients_ofFn _ (by
    rw [eigenDifferencePolynomial_degree]
    simp only [Fintype.card_fin, pow_two]
    omega)

theorem eigenComparisonGap_pos {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    0 < eigenComparisonGap A B := separationFromCoefficients_pos _

def eigenComparisonDepth {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) : ℕ :=
  eigenBisectionDepth (eigenSearchRadius A B) (eigenComparisonGap A B)

/-- The result is decided by finite rational arithmetic, including the equality case. -/
def compareMinimumEigenvalues {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) : Ordering :=
  let R := eigenSearchRadius A B
  let δ := eigenComparisonGap A B
  let t := eigenComparisonDepth A B
  let x := dyadicLower (eigenThresholdTest A) R t
  let y := dyadicLower (eigenThresholdTest B) R t
  let w := R / (2:ℚ)^t
  if δ-w ≤ x-y then .gt else if δ-w ≤ y-x then .lt else .eq

/-- Correctness includes exact ties and repeated eigenvalues. There is no
separation, eigensolver, or exact-real-comparison premise. -/
theorem compareMinimumEigenvalues_correct {n : ℕ} [Nonempty (Fin n)]
    (A B : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) (hB : (ratMatrixReal B).PosSemidef) :
    (compareMinimumEigenvalues A B = .eq ↔
      minimumEigenvalue (ratMatrixReal A) = minimumEigenvalue (ratMatrixReal B)) ∧
    (compareMinimumEigenvalues A B = .lt ↔
      minimumEigenvalue (ratMatrixReal A) < minimumEigenvalue (ratMatrixReal B)) ∧
    (compareMinimumEigenvalues A B = .gt ↔
      minimumEigenvalue (ratMatrixReal B) < minimumEigenvalue (ratMatrixReal A)) := by
  let R := eigenSearchRadius A B
  let δ := eigenComparisonGap A B
  let t := eigenComparisonDepth A B
  let x := dyadicLower (eigenThresholdTest A) R t
  let y := dyadicLower (eigenThresholdTest B) R t
  let w := R / (2:ℚ)^t
  have hR := eigenSearchRadius_pos A B
  have hδ := eigenComparisonGap_pos A B
  have hBA : eigenSearchRadius B A = R := by simp only [R, eigenSearchRadius]; ring
  have ha := dyadicLower_bounds (eigenThresholdTest A) R hR
    (minimumEigenvalue_nonneg hA) (minimumEigenvalue_le_radius A B hA.isHermitian)
    (eigenThresholdTest_correct A hA.isHermitian) t
  have hb := dyadicLower_bounds (eigenThresholdTest B) R hR
    (minimumEigenvalue_nonneg hB)
    (by simpa only [hBA] using minimumEigenvalue_le_radius B A hB.isHermitian)
    (eigenThresholdTest_correct B hB.isHermitian) t
  have hw : (0 : ℝ) ≤ (w : ℝ) := by dsimp [w]; positivity
  have hn : 2*(w : ℝ) < (δ : ℝ) := by
    simpa only [w, t, eigenComparisonDepth, R, δ, Rat.cast_div,
      Rat.cast_pow, Rat.cast_ofNat, mul_div_assoc]
      using eigenBisectionDepth_narrow hR hδ
  have hs : ∀ ha : minimumEigenvalue (ratMatrixReal A) ≠ minimumEigenvalue (ratMatrixReal B),
      (δ : ℝ) ≤ |minimumEigenvalue (ratMatrixReal A) - minimumEigenvalue (ratMatrixReal B)| := by
    intro hh
    dsimp [δ]
    rw [eigenComparisonGap_eq]
    exact minimumEigenvalue_separation A B hA.isHermitian hB.isHermitian hh
  have ha' : (x : ℝ) ≤ minimumEigenvalue (ratMatrixReal A) ∧
      minimumEigenvalue (ratMatrixReal A) ≤ (x : ℝ) + (w : ℝ) := by
    simpa only [x, w, Rat.cast_div, Rat.cast_pow, Rat.cast_ofNat] using ha
  have hb' : (y : ℝ) ≤ minimumEigenvalue (ratMatrixReal B) ∧
      minimumEigenvalue (ratMatrixReal B) ≤ (y : ℝ) + (w : ℝ) := by
    simpa only [y, w, Rat.cast_div, Rat.cast_pow, Rat.cast_ofNat] using hb
  have hc := compare_of_approximations (by exact_mod_cast hδ) hw hn ha' hb' hs
  change ((if δ-w ≤ x-y then Ordering.gt else if δ-w ≤ y-x then .lt else .eq) = .eq ↔ _) ∧ _
  by_cases hg : δ-w ≤ x-y
  · have hgr : (δ : ℝ)-(w : ℝ) ≤ (x : ℝ)-(y : ℝ) := by exact_mod_cast hg
    have hlt := hc.2.1 hgr
    simp only [if_pos hg, compareMinimumEigenvalues]
    change (Ordering.gt = Ordering.eq ↔ _) ∧
      ((if δ-w ≤ x-y then Ordering.gt else if δ-w ≤ y-x then .lt else .eq) = .lt ↔ _) ∧
      ((if δ-w ≤ x-y then Ordering.gt else if δ-w ≤ y-x then .lt else .eq) = .gt ↔ _)
    simp [hg, hlt.ne', hlt, not_lt.mpr hlt.le]
  · by_cases hl : δ-w ≤ y-x
    · have hlr : (δ : ℝ)-(w : ℝ) ≤ (y : ℝ)-(x : ℝ) := by exact_mod_cast hl
      have hlt := hc.2.2 hlr
      change ((if δ-w ≤ x-y then Ordering.gt else if δ-w ≤ y-x then .lt else .eq) = .eq ↔ _) ∧
        ((if δ-w ≤ x-y then Ordering.gt else if δ-w ≤ y-x then .lt else .eq) = .lt ↔ _) ∧
        ((if δ-w ≤ x-y then Ordering.gt else if δ-w ≤ y-x then .lt else .eq) = .gt ↔ _)
      simp [hg, hl, hlt.ne, hlt, not_lt.mpr hlt.le]
    · have hgr : (x : ℝ)-(y : ℝ) < (δ : ℝ)-(w : ℝ) := by exact_mod_cast lt_of_not_ge hg
      have hlr : (y : ℝ)-(x : ℝ) < (δ : ℝ)-(w : ℝ) := by exact_mod_cast lt_of_not_ge hl
      have he := hc.1.mpr (abs_lt.mpr ⟨by linarith, hgr⟩)
      change ((if δ-w ≤ x-y then Ordering.gt else if δ-w ≤ y-x then .lt else .eq) = .eq ↔ _) ∧
        ((if δ-w ≤ x-y then Ordering.gt else if δ-w ≤ y-x then .lt else .eq) = .lt ↔ _) ∧
        ((if δ-w ≤ x-y then Ordering.gt else if δ-w ≤ y-x then .lt else .eq) = .gt ↔ _)
      simp [hg, hl, he]

/-- Boolean comparison suitable for a finite candidate scan. -/
def minimumEigenvalueLE {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) : Bool :=
  compareMinimumEigenvalues A B != Ordering.gt

theorem minimumEigenvalueLE_correct {n : ℕ} [Nonempty (Fin n)]
    (A B : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) (hB : (ratMatrixReal B).PosSemidef) :
    minimumEigenvalueLE A B = true ↔
      minimumEigenvalue (ratMatrixReal A) ≤ minimumEigenvalue (ratMatrixReal B) := by
  have hh := (compareMinimumEigenvalues_correct A B hA hB).2.2
  simp only [minimumEigenvalueLE, bne_iff_ne, ne_eq, hh, not_lt]

end DAGSpectral
