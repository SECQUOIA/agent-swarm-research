import CertifiedMinlp.Quadratic
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Analysis.Convex.Function
import Mathlib.Tactic

/-! The square root of a positive semidefinite homogenized quadratic is convex.
The PSD hypothesis permits singular matrices and zero quadratic values. -/
namespace CertifiedMinlp

open Matrix

variable {n : Type*} [Fintype n]

/-- Append the constant coordinate used by a homogenized quadratic. -/
def homogenize (x : n → ℝ) : Option n → ℝ := Option.elim' 1 x

/-- The quadratic represented by a homogenized real matrix. -/
def homogenizedQuadratic (H : Matrix (Option n) (Option n) ℝ) (x : n → ℝ) : ℝ :=
  homogenize x ⬝ᵥ (H *ᵥ homogenize x)

theorem homogenizedQuadratic_nonneg {H : Matrix (Option n) (Option n) ℝ}
    (hH : H.PosSemidef) (x : n → ℝ) : 0 ≤ homogenizedQuadratic H x := by
  simpa [homogenizedQuadratic] using hH.dotProduct_mulVec_nonneg (homogenize x)

private theorem psd_norm_eq {m : Type*} [Fintype m] (H : Matrix m m ℝ)
    (hH : H.PosSemidef) (x : m → ℝ) :
    @norm (m → ℝ) (H.toSeminormedAddCommGroup hH).toNorm x =
      Real.sqrt (x ⬝ᵥ (H *ᵥ x)) := by
  change Real.sqrt (RCLike.re ((H *ᵥ x) ⬝ᵥ star x)) = _
  simp [dotProduct_comm]

private theorem psd_root_smul {m : Type*} [Fintype m]
    (H : Matrix m m ℝ) (x : m → ℝ) (a : ℝ) (ha : 0 ≤ a) :
    Real.sqrt ((a • x) ⬝ᵥ (H *ᵥ (a • x))) =
      a * Real.sqrt (x ⬝ᵥ (H *ᵥ x)) := by
  rw [Matrix.mulVec_smul, dotProduct_smul, smul_dotProduct]
  simp only [smul_eq_mul]
  rw [← mul_assoc, Real.sqrt_mul (mul_self_nonneg a), Real.sqrt_mul_self ha]

/-- Global convexity of the square root of a PSD homogenized quadratic. -/
theorem convexOn_sqrt_homogenizedQuadratic
    {H : Matrix (Option n) (Option n) ℝ} (hH : H.PosSemidef) :
    ConvexOn ℝ Set.univ (fun x : n → ℝ => Real.sqrt (homogenizedQuadratic H x)) := by
  refine ⟨convex_univ, ?_⟩
  intro x _ y _ a b ha hb hab
  have heq : homogenize (a • x + b • y) = a • homogenize x + b • homogenize y := by
    funext i
    cases i with
    | none => simpa [homogenize] using hab.symm
    | some i => rfl
  change Real.sqrt (homogenizedQuadratic H (a • x + b • y)) ≤ _
  unfold homogenizedQuadratic
  rw [heq]
  have ht := @norm_add_le (Option n → ℝ)
    (H.toSeminormedAddCommGroup hH).toSeminormedAddGroup
    (a • homogenize x) (b • homogenize y)
  simp only [psd_norm_eq H hH] at ht
  rw [psd_root_smul H _ a ha, psd_root_smul H _ b hb] at ht
  exact ht

/-- The conventional block matrix for `xᵀ Q x + bᵀ x + c`. -/
noncomputable def quadraticHomogenization (Q : Matrix n n ℝ) (b : n → ℝ) (c : ℝ) :
    Matrix (Option n) (Option n) ℝ
  | none, none => c
  | none, some j => b j / 2
  | some i, none => b i / 2
  | some i, some j => Q i j

/-- Homogenization is exactly the source quadratic, including its linear term. -/
theorem homogenizedQuadratic_blocks (Q : Matrix n n ℝ) (b x : n → ℝ) (c : ℝ) :
    homogenizedQuadratic (quadraticHomogenization Q b c) x =
      x ⬝ᵥ (Q *ᵥ x) + b ⬝ᵥ x + c := by
  simp only [homogenizedQuadratic, dotProduct, Matrix.mulVec, Fintype.sum_option,
    homogenize, Option.elim', quadraticHomogenization, mul_one, one_mul]
  simp only [mul_add, Finset.sum_add_distrib]
  have hhalf : ∑ i, x i * (b i / 2) = (∑ i, b i * x i) / 2 := by
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i _
    ring
  have hhalf' : ∑ i, b i / 2 * x i = (∑ i, b i * x i) / 2 := by
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hhalf, hhalf']
  ring

/-- A PSD homogenized matrix gives the square-root quadratic's curvature. -/
theorem convexOn_sqrt_quadratic {Q : Matrix n n ℝ} {b : n → ℝ} {c : ℝ}
    (hH : (quadraticHomogenization Q b c).PosSemidef) :
    ConvexOn ℝ Set.univ (fun x => Real.sqrt (x ⬝ᵥ (Q *ᵥ x) + b ⬝ᵥ x + c)) := by
  simpa only [homogenizedQuadratic_blocks] using convexOn_sqrt_homogenizedQuadratic hH

theorem quadratic_nonneg_of_homogenization_psd {Q : Matrix n n ℝ} {b : n → ℝ} {c : ℝ}
    (hH : (quadraticHomogenization Q b c).PosSemidef) (x : n → ℝ) :
    0 ≤ x ⬝ᵥ (Q *ᵥ x) + b ⬝ᵥ x + c := by
  simpa only [homogenizedQuadratic_blocks] using homogenizedQuadratic_nonneg hH x

/-- The PSD homogenization rule in the shared quadratic syntax. -/
theorem quadratic_sqrt_convex [DecidableEq n] {Q : Matrix n n ℝ}
    {b : n → ℝ} {c : ℝ} (hH : (quadraticHomogenization Q b c).PosSemidef) :
    ConvexOn ℝ Set.univ (fun x => Real.sqrt (quadratic Q b c x)) := by
  simpa only [quadratic_eq_matrix] using convexOn_sqrt_quadratic hH

/-- The same test certifies every square-root argument is nonnegative. -/
theorem quadratic_nonneg_of_psd_homogenization [DecidableEq n] {Q : Matrix n n ℝ}
    {b : n → ℝ} {c : ℝ} (hH : (quadraticHomogenization Q b c).PosSemidef) (x : n → ℝ) :
    0 ≤ quadratic Q b c x := by
  simpa only [quadratic_eq_matrix] using quadratic_nonneg_of_homogenization_psd hH x

end CertifiedMinlp
