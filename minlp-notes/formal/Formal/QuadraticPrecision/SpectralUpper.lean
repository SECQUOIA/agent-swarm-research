import Formal.QuadraticPrecision.Spectral
import Formal.QuadraticPrecision.UpperSquares
import Formal.QuadraticPrecision.LowerContact
import Formal.QuadraticPrecision.OutputReflection

open scoped BigOperators Matrix
open Matrix
namespace QuadraticPrecision
noncomputable section
variable {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}

/-- Total absolute curvature after affine normalization on the given box. -/
def spectralWeight (hH : H.IsHermitian) (l u : Input n) : ℝ :=
  ∑ j : {j // hH.eigenvalues j ≠ 0}, |spectralCoefficient hH l u j|

theorem spectralWeight_nonneg (hH : H.IsHermitian) (l u : Input n) :
    0 ≤ spectralWeight hH l u := Finset.sum_nonneg (fun _ _ => abs_nonneg _)

theorem spectralWeight_pos (hH : H.IsHermitian) (l u : Input n) (hr : 0 < H.rank) :
    0 < spectralWeight hH l u := spectral_totalWeight_pos hH l u hr

theorem spectral_polynomial_decomposition (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) :
    quadraticPolynomial H a b = fun x => spectralAffineMap hH a b l u x +
      ∑ j : {j // hH.eigenvalues j ≠ 0},
        spectralCoefficient hH l u j * spectralNormalizedMap hH l u j x ^ 2 := by
  funext x
  simpa only [quadraticPolynomial, contactQuadratic, dotProduct_comm] using
    spectral_signed_decomposition_nonzero hH a b l u x

/-- An actual binary linear graph lift with rank times depth binaries. -/
theorem quadratic_graph_binary_upper (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (L : ℕ) :
    HasBinaryGraphLift {x | ∀ i, x i ∈ Set.Icc (l i) (u i)}
      (quadraticPolynomial H a b)
      (spectralWeight hH l u * (squareWidth L)^2 / 4) (H.rank * L) := by
  have ht := signedSquares_graph (UpperAssembly.boxSystem l u)
    (fun j : {j // hH.eigenvalues j ≠ 0} => spectralNormalizedMap hH l u j)
    (spectralAffineMap hH a b l u) (fun j => spectralCoefficient hH l u j) L
    (by
      intro x hx j
      simpa only [spectralNormalizedMap_apply] using
        spectralNormalized_mem hH l u j x ((UpperAssembly.boxSystem_feasible l u x).mp hx))
  have hd : (UpperAssembly.boxSystem l u).feasible =
      {x | ∀ i, x i ∈ Set.Icc (l i) (u i)} := by
    ext x
    exact UpperAssembly.boxSystem_feasible l u x
  rw [hd, ← spectral_polynomial_decomposition hH a l u b, ← spectral_rank hH] at ht
  exact ht

/-- Only negative normalized squares use binaries in the epigraph lift. -/
theorem quadratic_epigraph_binary_upper (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (L : ℕ) :
    HasBinaryEpigraphLift {x | ∀ i, x i ∈ Set.Icc (l i) (u i)}
      (quadraticPolynomial H a b)
      (spectralWeight hH l u * (squareWidth L)^2 / 4) (negativeInertia hH * L) := by
  have ht := signedSquares_epigraph (UpperAssembly.boxSystem l u)
    (fun j : {j // hH.eigenvalues j ≠ 0} => spectralNormalizedMap hH l u j)
    (spectralAffineMap hH a b l u) (fun j => spectralCoefficient hH l u j) L
    (by
      intro x hx j
      simpa only [spectralNormalizedMap_apply] using
        spectralNormalized_mem hH l u j x ((UpperAssembly.boxSystem_feasible l u x).mp hx))
  have hd : (UpperAssembly.boxSystem l u).feasible =
      {x | ∀ i, x i ∈ Set.Icc (l i) (u i)} := by
    ext x
    exact UpperAssembly.boxSystem_feasible l u x
  rw [hd, ← spectral_polynomial_decomposition hH a l u b, spectral_negative_count hH l u] at ht
  exact ht

/-- Reflection of the signed-square construction counts positive eigenvalues
without choosing or assuming an eigenbasis for the negated matrix. -/
theorem quadratic_hypograph_binary_upper (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (L : ℕ) :
    HasBinaryHypographLift {x | ∀ i, x i ∈ Set.Icc (l i) (u i)}
      (quadraticPolynomial H a b)
      (spectralWeight hH l u * (squareWidth L)^2 / 4) (positiveInertia hH * L) := by
  have ht := signedSquares_epigraph (UpperAssembly.boxSystem l u)
    (fun j : {j // hH.eigenvalues j ≠ 0} => spectralNormalizedMap hH l u j)
    (-spectralAffineMap hH a b l u) (fun j => -spectralCoefficient hH l u j) L
    (by
      intro x hx j
      simpa only [spectralNormalizedMap_apply] using
        spectralNormalized_mem hH l u j x ((UpperAssembly.boxSystem_feasible l u x).mp hx))
  have hn := ht.neg
  have hd : (UpperAssembly.boxSystem l u).feasible =
      {x | ∀ i, x i ∈ Set.Icc (l i) (u i)} := by
    ext x
    exact UpperAssembly.boxSystem_feasible l u x
  have hf : (fun x => -((-spectralAffineMap hH a b l u) x +
        ∑ j : {j // hH.eigenvalues j ≠ 0},
          -spectralCoefficient hH l u j * spectralNormalizedMap hH l u j x ^ 2)) =
      quadraticPolynomial H a b := by
    rw [spectral_polynomial_decomposition hH a l u b]
    funext x
    simp [Finset.sum_neg_distrib, add_comm]
  have hc : Fintype.card {j : {j // hH.eigenvalues j ≠ 0} //
      -spectralCoefficient hH l u j < 0} = positiveInertia hH := by
    simp only [neg_neg_iff_pos]
    exact spectral_positive_count hH l u
  rw [hd, hf, hc] at hn
  simpa only [abs_neg, spectralWeight] using hn

def quadraticGraphLift (hH : H.IsHermitian) (a l u : Input n) (b : ℝ) (L : ℕ) :=
  signedSquaresGraphLift (UpperAssembly.boxSystem l u)
    (fun j : {j // hH.eigenvalues j ≠ 0} => spectralNormalizedMap hH l u j)
    (spectralAffineMap hH a b l u) (fun j => spectralCoefficient hH l u j) L

def quadraticEpigraphLift (hH : H.IsHermitian) (a l u : Input n) (b : ℝ) (L : ℕ) :=
  signedSquaresEpigraphLift (UpperAssembly.boxSystem l u)
    (fun j : {j // hH.eigenvalues j ≠ 0} => spectralNormalizedMap hH l u j)
    (spectralAffineMap hH a b l u) (fun j => spectralCoefficient hH l u j) L

theorem quadraticGraphLift_rowCount (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (L : ℕ) :
    (quadraticGraphLift hH a l u b L).system.rowCount =
      2*n + H.rank * (11+L*10) + 2 := by
  rw [quadraticGraphLift, signedSquaresGraphLift_rowCount, ← spectral_rank hH]
  simp only [UpperAssembly.boxSystem]
  omega

theorem quadraticEpigraphLift_rowCount_le (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (L : ℕ) :
    (quadraticEpigraphLift hH a l u b L).system.rowCount ≤
      2*n + H.rank * (11+L*10) + 2 := by
  have hh := signedSquaresEpigraphLift_rowCount_le (UpperAssembly.boxSystem l u)
    (fun j : {j // hH.eigenvalues j ≠ 0} => spectralNormalizedMap hH l u j)
    (spectralAffineMap hH a b l u) (fun j => spectralCoefficient hH l u j) L
  rw [← spectral_rank hH] at hh
  simpa only [quadraticEpigraphLift, UpperAssembly.boxSystem, two_mul] using hh

def quadraticHypographLift (hH : H.IsHermitian) (a l u : Input n) (b : ℝ) (L : ℕ) :=
  (signedSquaresEpigraphLift (UpperAssembly.boxSystem l u)
    (fun j : {j // hH.eigenvalues j ≠ 0} => spectralNormalizedMap hH l u j)
    (-spectralAffineMap hH a b l u) (fun j => -spectralCoefficient hH l u j) L).reflect

theorem quadraticHypographLift_rowCount_le (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (L : ℕ) :
    (quadraticHypographLift hH a l u b L).system.rowCount ≤
      2*n + H.rank * (11+L*10) + 2 := by
  have hh := signedSquaresEpigraphLift_rowCount_le (UpperAssembly.boxSystem l u)
    (fun j : {j // hH.eigenvalues j ≠ 0} => spectralNormalizedMap hH l u j)
    (-spectralAffineMap hH a b l u) (fun j => -spectralCoefficient hH l u j) L
  rw [← spectral_rank hH] at hh
  simpa only [quadraticHypographLift, BinaryLinearLift.reflect_rowCount,
    UpperAssembly.boxSystem, two_mul] using hh

theorem quadraticGraphLift_auxCount (hH : H.IsHermitian) (L : ℕ) :
    Fintype.card (UpperAssembly.AuxIndex
      (fun _ : {j // hH.eigenvalues j ≠ 0} => 2 + (L + L))) =
      H.rank * (3 + 2 * L) := by
  rw [signedSquaresGraphLift_auxCount, ← spectral_rank hH]

theorem quadraticEpigraphLift_auxCount_le (hH : H.IsHermitian)
    (l u : Input n) (L : ℕ) :
    Fintype.card (UpperAssembly.AuxIndex (SignedEpigraph.auxiliaries
      (fun j : {j // hH.eigenvalues j ≠ 0} => spectralCoefficient hH l u j) L)) ≤
      H.rank * (3 + 2 * L) := by
  simpa only [spectral_rank hH] using SignedEpigraph.auxiliaries_count_le
    (fun j : {j // hH.eigenvalues j ≠ 0} => spectralCoefficient hH l u j) L

theorem quadraticHypographLift_auxCount_le (hH : H.IsHermitian)
    (l u : Input n) (L : ℕ) :
    Fintype.card (UpperAssembly.AuxIndex (SignedEpigraph.auxiliaries
      (fun j : {j // hH.eigenvalues j ≠ 0} => -spectralCoefficient hH l u j) L)) ≤
      H.rank * (3 + 2 * L) := by
  simpa only [spectral_rank hH] using SignedEpigraph.auxiliaries_count_le
    (fun j : {j // hH.eigenvalues j ≠ 0} => -spectralCoefficient hH l u j) L

private theorem count_sum_ite {J : Type*} [Fintype J] (p : J → Prop)
    [DecidablePred p] (a b : ℕ) :
    (∑ j, if p j then a else b) =
      Fintype.card {j // p j} * a + (Fintype.card J - Fintype.card {j // p j}) * b := by
  rw [← Fintype.sum_subtype_add_sum_subtype p (fun j => if p j then a else b)]
  have hpos : (∑ i : {j // p j}, if p i then a else b) = Fintype.card {j // p j} * a := by
    simp only [Subtype.property, ite_true, Finset.sum_const, Finset.card_univ, smul_eq_mul]
  have hneg : (∑ i : {j // ¬p j}, if p i then a else b) = Fintype.card {j // ¬p j} * b := by
    have he (i : {j // ¬p j}) : (if p i then a else b) = b := if_neg i.property
    simp_rw [he]
    simp
  rw [hpos, hneg, Fintype.card_subtype_compl]

theorem quadraticEpigraphLift_rowCount (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (L : ℕ) :
    (quadraticEpigraphLift hH a l u b L).system.rowCount =
      2*n + (negativeInertia hH * (11+L*10) +
        (H.rank-negativeInertia hH) * (3*L+3)) + 2 := by
  rw [quadraticEpigraphLift, signedSquaresEpigraphLift_rowCount, count_sum_ite,
    spectral_negative_count hH l u, ← spectral_rank hH]
  simp [UpperAssembly.boxSystem, two_mul]

theorem quadraticHypographLift_rowCount (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (L : ℕ) :
    (quadraticHypographLift hH a l u b L).system.rowCount =
      2*n + (positiveInertia hH * (11+L*10) +
        (H.rank-positiveInertia hH) * (3*L+3)) + 2 := by
  rw [quadraticHypographLift, BinaryLinearLift.reflect_rowCount,
    signedSquaresEpigraphLift_rowCount]
  simp only [neg_neg_iff_pos]
  rw [count_sum_ite, spectral_positive_count hH l u, ← spectral_rank hH]
  simp [UpperAssembly.boxSystem, two_mul]

theorem quadraticEpigraphLift_auxCount (hH : H.IsHermitian)
    (l u : Input n) (L : ℕ) :
    Fintype.card (UpperAssembly.AuxIndex (SignedEpigraph.auxiliaries
      (fun j : {j // hH.eigenvalues j ≠ 0} => spectralCoefficient hH l u j) L)) =
      negativeInertia hH * (3+2*L) + (H.rank-negativeInertia hH)*(L+1) := by
  rw [UpperAssembly.aux_count]
  simp only [SignedEpigraph.auxiliaries_eq]
  simp_rw [ite_add]
  rw [count_sum_ite, spectral_negative_count hH l u, ← spectral_rank hH]
  congr 2
  omega

theorem quadraticHypographLift_auxCount (hH : H.IsHermitian)
    (l u : Input n) (L : ℕ) :
    Fintype.card (UpperAssembly.AuxIndex (SignedEpigraph.auxiliaries
      (fun j : {j // hH.eigenvalues j ≠ 0} => -spectralCoefficient hH l u j) L)) =
      positiveInertia hH * (3+2*L) + (H.rank-positiveInertia hH)*(L+1) := by
  rw [UpperAssembly.aux_count]
  simp only [SignedEpigraph.auxiliaries_eq, neg_neg_iff_pos]
  simp_rw [ite_add]
  rw [count_sum_ite, spectral_positive_count hH l u, ← spectral_rank hH]
  congr 2
  omega

end
end QuadraticPrecision
