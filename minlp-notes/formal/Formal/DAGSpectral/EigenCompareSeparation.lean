import Mathlib.Algebra.Polynomial.Degree.TrailingDegree
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Tactic

/-! Explicit coefficient-height separation of nonzero polynomial roots from zero. -/
namespace DAGSpectral
open Polynomial
open scoped BigOperators

/-- The integer coefficient one-norm, computed by a finite sum. -/
def intPolynomialHeight (P : ℤ[X]) : ℕ :=
  ∑ k ∈ P.support, (P.coeff k).natAbs

lemma root_trailingCoeff_bound {R : Type*} [Semiring R] (f : R →+* ℝ)
    {P : R[X]} (hP : P ≠ 0) {α : ℝ} (hα : α ≠ 0) (hα1 : |α| ≤ 1)
    (hroot : P.eval₂ f α = 0) :
    |f P.trailingCoeff| ≤ (∑ i ∈ P.support, |f (P.coeff i)|) * |α| := by
  classical
  let k := P.natTrailingDegree
  have hk0 : P.coeff k ≠ 0 := (Polynomial.trailingCoeff_eq_zero.not.mpr hP)
  have hk : k ∈ P.support := Polynomial.mem_support_iff.mpr hk0
  have heval : ∑ i ∈ P.support, f (P.coeff i) * α ^ i = 0 := by
    simpa only [Polynomial.eval₂_eq_sum, Polynomial.sum_def] using hroot
  have heq := Finset.sum_erase_add P.support (fun i => f (P.coeff i) * α ^ i) hk
  rw [heval] at heq
  have hterm : |f (P.coeff k) * α ^ k| ≤
      ∑ i ∈ P.support.erase k, |f (P.coeff i) * α ^ i| := by
    have ht : f (P.coeff k) * α ^ k =
        -(∑ i ∈ P.support.erase k, f (P.coeff i) * α ^ i) := by linarith
    rw [ht, abs_neg]
    exact Finset.abs_sum_le_sum_abs _ _
  have hsum : (∑ i ∈ P.support.erase k, |f (P.coeff i) * α ^ i|) ≤
      (∑ i ∈ P.support, |f (P.coeff i)|) * |α| ^ (k + 1) := by
    calc
      _ ≤ ∑ i ∈ P.support.erase k, |f (P.coeff i)| * |α| ^ (k + 1) := by
        apply Finset.sum_le_sum
        intro i hi
        obtain ⟨hik, hiP⟩ := Finset.mem_erase.mp hi
        have hki : k < i := lt_of_le_of_ne
          (Polynomial.natTrailingDegree_le_of_ne_zero (Polynomial.mem_support_iff.mp hiP))
          (Ne.symm hik)
        rw [abs_mul, abs_pow]
        exact mul_le_mul_of_nonneg_left
          (pow_le_pow_of_le_one (abs_nonneg α) hα1 (Nat.succ_le_of_lt hki)) (abs_nonneg _)
      _ ≤ ∑ i ∈ P.support, |f (P.coeff i)| * |α| ^ (k + 1) := by
        exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.erase_subset _ _)
          (fun _ _ _ => mul_nonneg (abs_nonneg _) (pow_nonneg (abs_nonneg _) _))
      _ = _ := by rw [Finset.sum_mul]
  have hp : 0 < |α| ^ k := pow_pos (abs_pos.mpr hα) _
  apply (mul_le_mul_iff_left₀ hp).mp
  have h := hterm.trans hsum
  simpa only [abs_mul, abs_pow, pow_succ, mul_assoc, mul_left_comm, mul_comm,
    Polynomial.trailingCoeff, k] using h

lemma intPolynomialHeight_pos {P : ℤ[X]} (hP : P ≠ 0) : 0 < intPolynomialHeight P := by
  classical
  apply Finset.sum_pos' (fun _ _ => Nat.zero_le _)
  have hk : P.natTrailingDegree ∈ P.support :=
    Polynomial.mem_support_iff.mpr (Polynomial.trailingCoeff_eq_zero.not.mpr hP)
  exact ⟨_, hk, Int.natAbs_pos.mpr (Polynomial.trailingCoeff_eq_zero.not.mpr hP)⟩

lemma intPolynomialHeight_cast (P : ℤ[X]) :
    (intPolynomialHeight P : ℝ) = ∑ i ∈ P.support, |(P.coeff i : ℝ)| := by
  simp only [intPolynomialHeight, Nat.cast_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [← Int.cast_abs, ← Int.natCast_natAbs, Int.cast_natCast]

/-- A nonzero real root of a nonzero integer polynomial cannot approach zero
more closely than the reciprocal coefficient height, even with a zero constant term. -/
theorem intPolynomial_nonzero_root_bound {P : ℤ[X]} (hP : P ≠ 0) {α : ℝ}
    (hα : α ≠ 0) (hroot : P.eval₂ (Int.castRingHom ℝ) α = 0) :
    1 / max 1 (intPolynomialHeight P : ℝ) ≤ |α| := by
  have hH : (1 : ℝ) ≤ intPolynomialHeight P := by
    exact_mod_cast intPolynomialHeight_pos hP
  rw [max_eq_right hH]
  by_cases hα1 : |α| ≤ 1
  · have hb := root_trailingCoeff_bound (Int.castRingHom ℝ) hP hα hα1 hroot
    have hc : (1 : ℝ) ≤ |(P.trailingCoeff : ℝ)| := by
      have hn : 1 ≤ P.trailingCoeff.natAbs := Int.natAbs_pos.mpr
        (Polynomial.trailingCoeff_eq_zero.not.mpr hP)
      have hh : (P.trailingCoeff.natAbs : ℝ) = |(P.trailingCoeff : ℝ)| := by
        rw [← Int.cast_abs, ← Int.natCast_natAbs, Int.cast_natCast]
      rw [← hh]
      exact_mod_cast hn
    apply (div_le_iff₀ (lt_of_lt_of_le zero_lt_one hH)).mpr
    rw [intPolynomialHeight_cast]
    simpa only [Int.coe_castRingHom, mul_comm] using hc.trans hb
  · exact (div_le_one (lt_of_lt_of_le zero_lt_one hH)).mpr hH |>.trans (le_of_not_ge hα1)


/-- A common coefficient denominator, computed without polynomial factorization. -/
def ratPolynomialDen (P : ℚ[X]) : ℕ := ∏ i ∈ P.support, (P.coeff i).den

def ratPolynomialHeight (P : ℚ[X]) : ℚ := ∑ i ∈ P.support, |P.coeff i|

/-- A positive rational separation radius, directly computable from coefficients. -/
def ratRootSeparation (P : ℚ[X]) : ℚ :=
  1 / ((ratPolynomialDen P : ℚ) * max 1 (ratPolynomialHeight P))

lemma ratPolynomialDen_pos (P : ℚ[X]) : 0 < ratPolynomialDen P :=
  Finset.prod_pos (fun i _ => (P.coeff i).den_pos)

lemma ratRootSeparation_pos (P : ℚ[X]) : 0 < ratRootSeparation P := by
  apply one_div_pos.mpr
  exact mul_pos (by exact_mod_cast ratPolynomialDen_pos P)
    (lt_of_lt_of_le zero_lt_one (le_max_left _ _))

lemma ratPolynomialHeight_cast (P : ℚ[X]) :
    (ratPolynomialHeight P : ℝ) = ∑ i ∈ P.support, |(P.coeff i : ℝ)| := by
  simp only [ratPolynomialHeight, Rat.cast_sum, Rat.cast_abs]

lemma ratPolynomialDen_coeff_bound {P : ℚ[X]} {k : ℕ} (hk : k ∈ P.support) :
    (1 : ℝ) ≤ (ratPolynomialDen P : ℝ) * |(P.coeff k : ℝ)| := by
  have hden : (P.coeff k).den ≤ ratPolynomialDen P := by
    unfold ratPolynomialDen
    exact Finset.single_le_prod' (f := fun i => (P.coeff i).den)
      (fun i _ => (P.coeff i).den_pos) hk
  have hnum : 1 ≤ (P.coeff k).num.natAbs :=
    Int.natAbs_pos.mpr (Rat.num_ne_zero.mpr (Polynomial.mem_support_iff.mp hk))
  have hc : (1 : ℝ) ≤ |((P.coeff k).num : ℝ)| := by
    have heq : ((P.coeff k).num.natAbs : ℝ) = |((P.coeff k).num : ℝ)| := by
      rw [← Int.cast_abs, ← Int.natCast_natAbs, Int.cast_natCast]
    rw [← heq]
    exact_mod_cast hnum
  have hdpos : (0 : ℝ) < (P.coeff k).den := by exact_mod_cast (P.coeff k).den_pos
  have hdle : ((P.coeff k).den : ℝ) ≤ ratPolynomialDen P := by exact_mod_cast hden
  rw [Rat.cast_def, abs_div, abs_of_pos hdpos, ← mul_div_assoc]
  apply (le_div_iff₀ hdpos).mpr
  have hDp : (0 : ℝ) ≤ ratPolynomialDen P := Nat.cast_nonneg _
  nlinarith

/-- Nonzero roots are separated from zero by a computable rational bound;
zero constant coefficients and repeated roots require no special assumptions. -/
theorem ratPolynomial_nonzero_root_bound {P : ℚ[X]} (hP : P ≠ 0) {α : ℝ}
    (hα : α ≠ 0) (hroot : P.eval₂ (Rat.castHom ℝ) α = 0) :
    (ratRootSeparation P : ℝ) ≤ |α| := by
  let D : ℝ := ratPolynomialDen P
  let H : ℝ := ratPolynomialHeight P
  have hDp : 0 < D := by dsimp [D]; exact_mod_cast ratPolynomialDen_pos P
  have hD1 : 1 ≤ D := by dsimp [D]; exact_mod_cast ratPolynomialDen_pos P
  have hm1 : (1 : ℝ) ≤ max 1 H := le_max_left _ _
  have hmp : 0 < max 1 H := zero_lt_one.trans_le hm1
  change ((1 / ((ratPolynomialDen P : ℚ) * max 1 (ratPolynomialHeight P)) : ℚ) : ℝ) ≤ |α|
  simp only [Rat.cast_div, Rat.cast_one, Rat.cast_mul, Rat.cast_natCast, Rat.cast_max]
  change 1 / (D * max 1 H) ≤ |α|
  apply (div_le_iff₀ (mul_pos hDp hmp)).mpr
  by_cases hα1 : |α| ≤ 1
  · have hb := root_trailingCoeff_bound (Rat.castHom ℝ) hP hα hα1 hroot
    have hk : P.natTrailingDegree ∈ P.support :=
      Polynomial.mem_support_iff.mpr (Polynomial.trailingCoeff_eq_zero.not.mpr hP)
    have hc := ratPolynomialDen_coeff_bound hk
    have hheight : (∑ i ∈ P.support, |(P.coeff i : ℝ)|) = H :=
      (ratPolynomialHeight_cast P).symm
    simp only [Rat.coe_castHom] at hb
    rw [hheight] at hb
    have hbound : |(P.trailingCoeff : ℝ)| ≤ max 1 H * |α| :=
      hb.trans (mul_le_mul_of_nonneg_right (le_max_right _ _) (abs_nonneg _))
    have hmul := mul_le_mul_of_nonneg_left hbound hDp.le
    change 1 ≤ D * |(P.trailingCoeff : ℝ)| at hc
    nlinarith
  · have ha : 1 ≤ |α| := le_of_not_ge hα1
    have hden : 1 ≤ D * max 1 H := by
      have hh := mul_le_mul hD1 hm1 (by norm_num : (0 : ℝ) ≤ 1) hDp.le
      simpa using hh
    nlinarith


/-- Executable gap formula on a coefficient list; trailing zero coefficients
are harmless because their denominator is one. -/
def separationFromCoefficients (xs : List ℚ) : ℚ :=
  1 / (((xs.map Rat.den).prod : ℚ) * max 1 ((xs.map abs).sum))

lemma separationFromCoefficients_pos (xs : List ℚ) :
    0 < separationFromCoefficients xs := by
  apply one_div_pos.mpr
  apply mul_pos
  · have hp : 0 < (xs.map Rat.den).prod := by
      apply List.prod_pos
      intro n hn
      obtain ⟨q, _, rfl⟩ := List.mem_map.mp hn
      exact q.den_pos
    exact_mod_cast hp
  · exact zero_lt_one.trans_le (le_max_left _ _)

lemma separationFromCoefficients_ofFn (P : ℚ[X]) {N : ℕ} (hN : P.natDegree < N) :
    separationFromCoefficients (List.ofFn (fun i : Fin N => P.coeff i)) =
      ratRootSeparation P := by
  have hs : P.support ⊆ Finset.range N := by
    intro i hi
    exact Finset.mem_range.mpr ((Polynomial.le_natDegree_of_ne_zero
      (Polynomial.mem_support_iff.mp hi)).trans_lt hN)
  have hprod : (∏ i ∈ P.support, (P.coeff i).den) =
      ∏ i ∈ Finset.range N, (P.coeff i).den :=
    Finset.prod_subset hs (by
      intro i _ hi
      simp [Polynomial.notMem_support_iff.mp hi])
  have hsum : (∑ i ∈ P.support, |P.coeff i|) =
      ∑ i ∈ Finset.range N, |P.coeff i| :=
    Finset.sum_subset hs (by
      intro i _ hi
      simp [Polynomial.notMem_support_iff.mp hi])
  simp only [separationFromCoefficients, List.map_ofFn, List.prod_ofFn, List.sum_ofFn,
    Function.comp_def, ratRootSeparation, ratPolynomialDen, ratPolynomialHeight, hprod, hsum]
  rw [Fin.prod_univ_eq_prod_range (fun i => (P.coeff i).den) N,
    Fin.sum_univ_eq_sum_range (fun i => |P.coeff i|) N]

lemma separationFromCoefficients_root_bound {P : ℚ[X]} {N : ℕ} (hN : P.natDegree < N)
    (hP : P ≠ 0) {α : ℝ} (hα : α ≠ 0)
    (hroot : P.eval₂ (Rat.castHom ℝ) α = 0) :
    (separationFromCoefficients (List.ofFn (fun i : Fin N => P.coeff i)) : ℝ) ≤ |α| := by
  rw [separationFromCoefficients_ofFn P hN]
  exact ratPolynomial_nonzero_root_bound hP hα hroot

end DAGSpectral
