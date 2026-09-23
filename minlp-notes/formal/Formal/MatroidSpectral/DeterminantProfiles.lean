import Formal.MatroidSpectral.Representation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic

/-! Exact characteristic-zero determinant profiles. Ordered minors occur only in the
proof; the defining polynomial is a determinant of a matrix of monomials. -/
namespace MatroidSpectral
open Matrix Finset
open scoped BigOperators

section CauchyBinet
variable {n m R : Type*} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]
  [CommRing R]

omit [DecidableEq m] in
theorem det_mul_rectangular (A : Matrix n m R) (B : Matrix m n R) :
    (A * B).det = ∑ f : n → m, (A.submatrix id f).det * ∏ i, B (f i) i := by
  classical
  simp only [Matrix.det_apply', Matrix.mul_apply, Finset.prod_univ_sum,
    Finset.mul_sum, Fintype.piFinset_univ]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro f _
  simp only [Matrix.submatrix_apply, id_eq, Finset.sum_mul, Finset.prod_mul_distrib]
  apply Finset.sum_congr rfl
  intro σ _
  ring

/-- Weighted Cauchy–Binet with ordered minors; each column set has the same
permutation multiplicity. Repeated-column minors vanish. -/
theorem weighted_cauchy_binet_ordered (A : Matrix n m R) (w : m → R) :
    (Fintype.card (Equiv.Perm n) : R) * (A * Matrix.diagonal w * A.transpose).det =
      ∑ f : n → m, (A.submatrix id f).det ^ 2 * ∏ i, w (f i) := by
  classical
  have hexp : (A * Matrix.diagonal w * A.transpose).det =
      ∑ f : n → m, (A.submatrix id f).det * (∏ i, w (f i)) * ∏ i, A i (f i) := by
    rw [Matrix.mul_assoc, det_mul_rectangular]
    simp only [Matrix.diagonal_mul, Matrix.transpose_apply, Finset.prod_mul_distrib]
    apply Finset.sum_congr rfl
    intro f _
    ring
  have hterm (σ : Equiv.Perm n) :
      (∑ f : n → m, (A.submatrix id f).det *
        (((Equiv.Perm.sign σ : ℤ) : R) * ∏ i, A (σ i) (f i)) * ∏ i, w (f i)) =
      (A * Matrix.diagonal w * A.transpose).det := by
    rw [hexp]
    let e : (n → m) ≃ (n → m) :=
      { toFun := fun f i => f (σ i)
        invFun := fun f i => f (σ.symm i)
        left_inv := by intro f; funext i; simp
        right_inv := by intro f; funext i; simp }
    symm
    apply Fintype.sum_equiv e
    intro f
    have hd : (A.submatrix id (e f)).det =
        (((Equiv.Perm.sign σ : ℤ) : R)) * (A.submatrix id f).det := by
      exact Matrix.det_permute' σ (A.submatrix id f)
    have hp : (∏ i, A (σ i) (e f i)) = ∏ i, A i (f i) := by
      exact Equiv.prod_comp σ (fun i => A i (f i))
    have hw : (∏ i, w (e f i)) = ∏ i, w (f i) := by
      exact Equiv.prod_comp σ (fun i => w (f i))
    rw [hd, hp, hw]
    have hs : (((Equiv.Perm.sign σ : ℤ) : R)) ^ 2 = 1 := by
      rcases Int.units_eq_one_or (Equiv.Perm.sign σ) with h | h <;> simp [h]
    symm
    calc
      _ = (((Equiv.Perm.sign σ : ℤ) : R)) ^ 2 *
          ((A.submatrix id f).det * (∏ i, w (f i)) * ∏ i, A i (f i)) := by ring
      _ = _ := by rw [hs, one_mul]
  calc
    _ = ∑ σ : Equiv.Perm n, (A * Matrix.diagonal w * A.transpose).det := by simp
    _ = ∑ σ : Equiv.Perm n, ∑ f : n → m, (A.submatrix id f).det *
        (((Equiv.Perm.sign σ : ℤ) : R) * ∏ i, A (σ i) (f i)) * ∏ i, w (f i) := by
      exact Finset.sum_congr rfl (fun σ _ => (hterm σ).symm)
    _ = _ := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro f _
      rw [pow_two, Matrix.det_apply' (A.submatrix id f)]
      simp only [Matrix.submatrix_apply, id_eq, Finset.sum_mul, Finset.mul_sum]

end CauchyBinet
noncomputable section Profiles
variable {q m : ℕ} {σ : Type*}

/-- The polynomial evaluated by the interpolation algorithm. -/
def determinantPolynomial (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → (σ →₀ ℕ)) : MvPolynomial σ ℚ :=
  let P := A.map MvPolynomial.C
  (P * Matrix.diagonal (fun e => MvPolynomial.monomial (w e) (1 : ℚ)) * P.transpose).det

def orderedProfile (w : Fin m → (σ →₀ ℕ)) (b : Fin q → Fin m) : σ →₀ ℕ :=
  ∑ i, w (b i)

/-- Rational squared minors prevent cancellation of bases sharing a profile. -/
theorem determinantPolynomial_identity (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → (σ →₀ ℕ)) :
    MvPolynomial.C (q.factorial : ℚ) * determinantPolynomial A w =
      ∑ b : Fin q → Fin m, MvPolynomial.monomial (orderedProfile w b)
        ((A.submatrix id b).det ^ 2) := by
  classical
  have h := weighted_cauchy_binet_ordered (A.map MvPolynomial.C)
    (fun e => MvPolynomial.monomial (w e) (1 : ℚ))
  simp only [Fintype.card_perm, Fintype.card_fin] at h
  rw [show MvPolynomial.C (q.factorial : ℚ) = (q.factorial : MvPolynomial σ ℚ) by simp]
  unfold determinantPolynomial
  rw [h]
  apply Finset.sum_congr rfl
  intro b _
  have hc : ((A.map (MvPolynomial.C : ℚ →+* MvPolynomial σ ℚ)).submatrix id b).det =
      MvPolynomial.C ((A.submatrix id b).det) :=
    (MvPolynomial.C.map_det (A.submatrix id b)).symm
  rw [hc, ← map_pow, orderedProfile, MvPolynomial.monomial_sum_index]

open Classical in
theorem determinantPolynomial_coeff_identity (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → (σ →₀ ℕ)) (z : σ →₀ ℕ) :
    (q.factorial : ℚ) * (determinantPolynomial A w).coeff z =
      ∑ b : Fin q → Fin m, if orderedProfile w b = z then
        (A.submatrix id b).det ^ 2 else 0 := by
  classical
  have h := congrArg (MvPolynomial.coeff z) (determinantPolynomial_identity A w)
  simpa only [MvPolynomial.coeff_C_mul, MvPolynomial.coeff_sum,
    MvPolynomial.coeff_monomial] using h

lemma factorial_rat_pos (q : ℕ) : (0 : ℚ) < q.factorial := by
  classical
  exact_mod_cast Nat.factorial_pos q

theorem determinantPolynomial_coeff_nonneg (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → (σ →₀ ℕ)) (z : σ →₀ ℕ) :
    0 ≤ (determinantPolynomial A w).coeff z := by
  classical
  apply (nonneg_of_mul_nonneg_left · (factorial_rat_pos q))
  rw [mul_comm, determinantPolynomial_coeff_identity]
  exact Finset.sum_nonneg (fun b _ => by split_ifs <;> positivity)

theorem determinantPolynomial_coeff_pos_iff (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → (σ →₀ ℕ)) (z : σ →₀ ℕ) :
    0 < (determinantPolynomial A w).coeff z ↔
      ∃ b : Fin q → Fin m, (A.submatrix id b).det ≠ 0 ∧ orderedProfile w b = z := by
  classical
  rw [← mul_pos_iff_of_pos_left (factorial_rat_pos q), determinantPolynomial_coeff_identity,
    Finset.sum_pos_iff_of_nonneg (fun b _ => by split_ifs <;> positivity)]
  simp only [Finset.mem_univ, true_and]
  constructor
  · rintro ⟨b, hb⟩
    by_cases h : orderedProfile w b = z
    · rw [if_pos h] at hb
      exact ⟨b, (sq_pos_iff.mp hb), h⟩
    · simp [h] at hb
  · rintro ⟨b, hb, hz⟩
    exact ⟨b, by simpa [hz] using sq_pos_of_ne_zero hb⟩

theorem determinantPolynomial_support_bound (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → (σ →₀ ℕ)) (W : ℕ) (hw : ∀ e i, w e i ≤ W)
    (z : σ →₀ ℕ) (hz : z ∈ (determinantPolynomial A w).support) :
    ∀ i, z i ≤ q * W := by
  classical
  have hpos : 0 < (determinantPolynomial A w).coeff z :=
    lt_of_le_of_ne (determinantPolynomial_coeff_nonneg A w z)
      (Ne.symm (MvPolynomial.mem_support_iff.mp hz))
  obtain ⟨b, _, rfl⟩ := (determinantPolynomial_coeff_pos_iff A w z).mp hpos
  intro i
  simp only [orderedProfile, Finsupp.coe_finsetSum, Finset.sum_apply]
  calc
    _ ≤ ∑ _j : Fin q, W := Finset.sum_le_sum (fun j _ => hw (b j) i)
    _ = q * W := by simp

/-- A profile sums the labels of the actual, unordered selected elements. -/
def baseProfile (w : Fin m → (σ →₀ ℕ)) (B : Finset (Fin m)) : σ →₀ ℕ :=
  ∑ e ∈ B, w e

lemma orderedProfile_eq_baseProfile (w : Fin m → (σ →₀ ℕ))
    (b : Fin q → Fin m) (hb : Function.Injective b) :
    orderedProfile w b = baseProfile w (Finset.univ.image b) := by
  classical
  simp only [orderedProfile, baseProfile, Finset.sum_image (fun i _ j _ hij => hb hij)]

theorem determinantPolynomial_coeff_pos_iff_base (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → (σ →₀ ℕ)) (z : σ →₀ ℕ) :
    0 < (determinantPolynomial A w).coeff z ↔
      ∃ B, IsBase A B ∧ baseProfile w B = z := by
  classical
  rw [determinantPolynomial_coeff_pos_iff]
  constructor
  · rintro ⟨b, hb, hz⟩
    exact ⟨Finset.univ.image b, (orderedMinor_isBase A b).mpr hb,
      (orderedProfile_eq_baseProfile w b (orderedMinor_injective A b hb)).symm.trans hz⟩
  · rintro ⟨B, hB, hz⟩
    obtain ⟨b, rfl, hb⟩ := hB.exists_orderedMinor
    exact ⟨b, hb, (orderedProfile_eq_baseProfile w b
      (orderedMinor_injective A b hb)).trans hz⟩

/-- Deletion zeros columns but keeps the original row count. -/
def retainedRepresentation (A : Matrix (Fin q) (Fin m) ℚ) (allowed : Finset (Fin m)) :
    Matrix (Fin q) (Fin m) ℚ := fun i e => if e ∈ allowed then A i e else 0

lemma retained_minor_iff (A : Matrix (Fin q) (Fin m) ℚ)
    (allowed : Finset (Fin m)) (b : Fin q → Fin m) :
    ((retainedRepresentation A allowed).submatrix id b).det ≠ 0 ↔
      (A.submatrix id b).det ≠ 0 ∧ ∀ i, b i ∈ allowed := by
  classical
  by_cases h : ∀ i, b i ∈ allowed
  · have heq : (retainedRepresentation A allowed).submatrix id b = A.submatrix id b := by
      ext i j
      simp [retainedRepresentation, h j]
    simp [heq, h]
  · obtain ⟨j, hj⟩ := not_forall.mp h
    have hz : ((retainedRepresentation A allowed).submatrix id b).det = 0 :=
      Matrix.det_eq_zero_of_column_eq_zero j (by
        intro i
        simp [retainedRepresentation, hj])
    simp [hz, h]

theorem retained_isBase_iff (A : Matrix (Fin q) (Fin m) ℚ)
    (allowed B : Finset (Fin m)) :
    IsBase (retainedRepresentation A allowed) B ↔ IsBase A B ∧ B ⊆ allowed := by
  classical
  constructor
  · intro hb
    obtain ⟨b, rfl, hminor⟩ := hb.exists_orderedMinor
    obtain ⟨hA, ha⟩ := (retained_minor_iff A allowed b).mp hminor
    refine ⟨(orderedMinor_isBase A b).mpr hA, ?_⟩
    intro e he
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp he
    exact ha i
  · rintro ⟨hb, ha⟩
    obtain ⟨b, rfl, hminor⟩ := hb.exists_orderedMinor
    apply (orderedMinor_isBase _ b).mpr
    exact (retained_minor_iff A allowed b).mpr ⟨hminor,
      fun i => ha (Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩)⟩

theorem determinantPolynomial_retained_coeff_pos_iff
    (A : Matrix (Fin q) (Fin m) ℚ) (allowed : Finset (Fin m))
    (w : Fin m → (σ →₀ ℕ)) (z : σ →₀ ℕ) :
    0 < (determinantPolynomial (retainedRepresentation A allowed) w).coeff z ↔
      ∃ B, IsBase A B ∧ B ⊆ allowed ∧ baseProfile w B = z := by
  classical
  simp only [determinantPolynomial_coeff_pos_iff_base, retained_isBase_iff]
  tauto

/-- Exact determinant evaluations use only rational matrix arithmetic. -/
theorem determinantPolynomial_eval [Fintype σ] (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → (σ →₀ ℕ)) (t : σ → ℚ) :
    MvPolynomial.eval t (determinantPolynomial A w) =
      (A * Matrix.diagonal (fun e => ∏ i, t i ^ (w e i)) * A.transpose).det := by
  classical
  unfold determinantPolynomial
  rw [RingHom.map_det]
  congr 1
  ext i j
  simp only [RingHom.mapMatrix_apply, Matrix.map_apply, Matrix.mul_apply,
    map_sum, map_mul, Matrix.transpose_apply, Matrix.diagonal_apply,
    MvPolynomial.eval_C]
  congr 1
  funext k
  congr 1
  congr 1
  funext e
  by_cases h : e = k
  · subst e
    simp only [if_pos, MvPolynomial.eval_monomial, one_mul]
    rw [Finsupp.prod_fintype _ _ (fun i => pow_zero (t i))]
  · simp [h]

end Profiles
end MatroidSpectral
