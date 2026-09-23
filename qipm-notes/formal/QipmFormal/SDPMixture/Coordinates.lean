import QipmFormal.Mixture.KKT
import QipmFormal.SDPMixture.Frobenius

/-!
# Frobenius-isometric coordinates for real symmetric matrices

A symmetric matrix is a symmetric vector in the Euclidean space indexed by
pairs of matrix indices. An orthonormal basis supplies the `svec` used in the
SDP residual estimates. It is constructed, rather than postulated.
-/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators

variable {n : Type*} [Fintype n]

/-- Symmetric matrices with their Frobenius inner product. -/
def symmetricSpace (n : Type*) [Fintype n] : Submodule ℝ (EuclideanSpace ℝ (n × n)) where
  carrier := {v | ∀ i j, v (i,j) = v (j,i)}
  zero_mem' := by simp
  add_mem' := by intro a b ha hb i j; simp only [PiLp.add_apply]; rw [ha, hb]
  smul_mem' := by intro a v hv i j; simp only [PiLp.smul_apply]; rw [hv]

abbrev SymmetricMatrix (n : Type*) [Fintype n] := symmetricSpace n

/-- Recover the entries of a symmetric matrix. -/
def toMatrix (X : SymmetricMatrix n) : Matrix n n ℝ := fun i j => X.val (i,j)

/-- Embed an actual symmetric matrix in the Frobenius space. -/
def ofMatrix (X : Matrix n n ℝ) (hX : X.IsSymm) : SymmetricMatrix n :=
  ⟨WithLp.toLp 2 (fun p : n × n => X p.1 p.2), fun i j => by
    exact congrFun (congrFun hX.symm i) j⟩

@[simp] theorem toMatrix_ofMatrix (X : Matrix n n ℝ) (hX : X.IsSymm) :
    toMatrix (ofMatrix X hX) = X := rfl

@[simp] theorem toMatrix_add (X Y : SymmetricMatrix n) :
    toMatrix (X + Y) = toMatrix X + toMatrix Y := rfl
@[simp] theorem toMatrix_sub (X Y : SymmetricMatrix n) :
    toMatrix (X - Y) = toMatrix X - toMatrix Y := rfl
@[simp] theorem toMatrix_smul (a : ℝ) (X : SymmetricMatrix n) :
    toMatrix (a • X) = a • toMatrix X := rfl
@[simp] theorem toMatrix_zero : toMatrix (0 : SymmetricMatrix n) = 0 := rfl

theorem toMatrix_isSymm (X : SymmetricMatrix n) : (toMatrix X).IsSymm := by
  ext i j
  exact X.property j i

/-- Symmetric matrices have one independent entry for each unordered index pair.
This equivalence is used only to compute dimension; `svec` below is isometric. -/
def symmetricEntriesEquiv (n : Type*) [Fintype n] :
    SymmetricMatrix n ≃ₗ[ℝ] (Sym2 n → ℝ) where
  toFun X := Sym2.lift ⟨toMatrix X, X.property⟩
  invFun v := ⟨WithLp.toLp 2 (fun p : n × n => v s(p.1, p.2)),
    fun i j => congrArg v Sym2.eq_swap⟩
  left_inv X := by
    apply Subtype.ext
    rfl
  right_inv v := funext <| Sym2.ind fun _ _ => rfl
  map_add' X Y := funext <| Sym2.ind fun _ _ => rfl
  map_smul' a X := funext <| Sym2.ind fun _ _ => rfl

/-- The constructed symmetric Frobenius space has the manuscript's svec dimension. -/
theorem finrank_symmetricMatrix : Module.finrank ℝ (SymmetricMatrix n) =
    Fintype.card n * (Fintype.card n + 1) / 2 := by
  rw [(symmetricEntriesEquiv n).finrank_eq, Module.finrank_fintype_fun_eq_card,
    Sym2.card, Nat.choose_two_right]
  simp [Nat.mul_comm]

/-- A canonical choice establishes existence of an isometric symmetric vectorization. -/
def symmetricBasis (n : Type*) [Fintype n] :
    OrthonormalBasis (Fin (Module.finrank ℝ (SymmetricMatrix n))) ℝ (SymmetricMatrix n) :=
  stdOrthonormalBasis ℝ (SymmetricMatrix n)

variable {J : Type*} [Fintype J]

/-- Coordinates in any fixed Frobenius-orthonormal basis. -/
def svec (e : OrthonormalBasis J ℝ (SymmetricMatrix n)) (X : SymmetricMatrix n) : J → ℝ :=
  fun j => e.repr X j

@[simp] theorem svec_add (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (X Y : SymmetricMatrix n) : svec e (X + Y) = svec e X + svec e Y := by
  funext j
  simp [svec]
@[simp] theorem svec_sub (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (X Y : SymmetricMatrix n) : svec e (X - Y) = svec e X - svec e Y := by
  funext j
  simp [svec]
@[simp] theorem svec_smul (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (a : ℝ) (X : SymmetricMatrix n) : svec e (a • X) = a • svec e X := by
  funext j
  simp [svec]

/-- Parseval's identity is exactly the matrix trace pairing on symmetric matrices. -/
theorem dot_svec (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (X Y : SymmetricMatrix n) :
    Mixture.dot (svec e X) (svec e Y) = Matrix.trace (toMatrix X * toMatrix Y) := by
  have h := e.repr.inner_map_map X Y
  have hs : (∑ j, svec e X j * svec e Y j) =
      ∑ p : n × n, X.val p * Y.val p := by
    change @inner ℝ (EuclideanSpace ℝ J) _ (e.repr X) (e.repr Y) =
      @inner ℝ (EuclideanSpace ℝ (n × n)) _ X.val Y.val at h
    simpa only [svec, EuclideanSpace.inner_eq_star_dotProduct, dotProduct,
      star_trivial, mul_comm] using h
  unfold Mixture.dot
  rw [hs, Fintype.sum_prod_type]
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply, toMatrix]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  rw [Y.property j i]

/-- Squared coordinate norm is the squared Frobenius norm. -/
theorem sqNorm_svec (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (X : SymmetricMatrix n) : Mixture.sqNorm (svec e X) =
      ∑ i, ∑ j, (toMatrix X i j)^2 := by
  unfold Mixture.sqNorm
  rw [show (∑ j, svec e X j ^ 2) = Mixture.dot (svec e X) (svec e X) by
    simp [Mixture.dot, pow_two], dot_svec]
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply, toMatrix, pow_two]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  rw [X.property j i]

/-- Coordinate Euclidean norm agrees with the intrinsic Frobenius norm. -/
theorem norm_svec (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (X : SymmetricMatrix n) : Mixture.euclideanNorm (svec e X) = ‖X‖ := by
  rw [Mixture.euclideanNorm_eq_norm_toLp]
  exact e.repr.norm_map X

/-- The matrix Frobenius norm equals the symmetric-space Hilbert norm. -/
theorem frobeniusNorm_toMatrix (X : SymmetricMatrix n) :
    frobeniusNorm (toMatrix X) = ‖X‖ := by
  rw [← norm_svec (symmetricBasis n), Mixture.euclideanNorm, sqNorm_svec]
  rfl

/-- Inverse vectorization reconstructs the symmetric matrix. -/
theorem svec_reconstruct (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (X : SymmetricMatrix n) : e.repr.symm (WithLp.toLp 2 (svec e X)) = X :=
  e.repr.symm_apply_apply X


/-- Every coordinate vector reconstructs to a symmetric matrix with those coordinates. -/
theorem svec_surjective (e : OrthonormalBasis J ℝ (SymmetricMatrix n)) :
    Function.Surjective (svec e) := by
  intro v
  refine ⟨e.repr.symm (WithLp.toLp 2 v), ?_⟩
  funext j
  simp [svec]

variable {I R : Type*} [Fintype I] [Fintype R]

/-- The convex combination in the symmetric Frobenius space. -/
def symmetricMix (w : I → ℝ) (X : I → SymmetricMatrix n) : SymmetricMatrix n :=
  ∑ i, w i • X i

theorem svec_mix (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (X : I → SymmetricMatrix n) :
    svec e (symmetricMix w X) = Mixture.mix w (fun i => svec e (X i)) := by
  funext j
  simp [svec, symmetricMix, Mixture.mix]

theorem toMatrix_mix (w : I → ℝ) (X : I → SymmetricMatrix n) :
    toMatrix (symmetricMix w X) = ∑ i, w i • toMatrix (X i) := by
  ext a b
  simp [toMatrix, symmetricMix, Matrix.sum_apply, Matrix.smul_apply]

/-- The SDP measurement map, specified by its symmetric measurement matrices. -/
def measurement (A : R → SymmetricMatrix n) (X : SymmetricMatrix n) : R → ℝ :=
  fun r => Matrix.trace (toMatrix (A r) * toMatrix X)

/-- The actual trace-adjoint measurement map. -/
def measurementAdjoint (A : R → SymmetricMatrix n) (y : R → ℝ) : SymmetricMatrix n :=
  ∑ r, y r • A r

/-- The matrix of the measurement map in the fixed isometric coordinates. -/
def coordinateMatrix (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) : R → J → ℝ := fun r => svec e (A r)

omit [Fintype R] in
theorem measurement_coordinates (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (X : SymmetricMatrix n) (r : R) :
    measurement A X r = ∑ j, coordinateMatrix e A r j * svec e X j :=
  (dot_svec e (A r) X).symm

theorem adjoint_coordinates (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (y : R → ℝ) (j : J) :
    svec e (measurementAdjoint A y) j = ∑ r, coordinateMatrix e A r j * y r := by
  simp [svec, measurementAdjoint, coordinateMatrix, mul_comm]

/-- The named adjoint satisfies the trace-adjoint identity. -/
theorem measurement_adjoint_identity (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (X : SymmetricMatrix n) (y : R → ℝ) :
    Matrix.trace (toMatrix (measurementAdjoint A y) * toMatrix X) =
      Mixture.dot y (measurement A X) := by
  rw [← dot_svec e]
  unfold Mixture.dot
  simp_rw [adjoint_coordinates, Finset.sum_mul, measurement_coordinates e]
  rw [Finset.sum_comm]
  simp only [Finset.mul_sum]
  congr 1
  funext r
  congr 1
  funext j
  ring

/-- Exact SDP centers have algebraic objective gap `r μ`. Coordinatewise
complementarity is neither assumed nor needed. -/
theorem sdp_objective_gap [DecidableEq n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (X S C : SymmetricMatrix n) (b y : R → ℝ)
    (μ : ℝ) (hp : measurement A X = b)
    (hd : measurementAdjoint A y + S = C)
    (hX : (toMatrix X).PosDef) (hc : toMatrix S = μ • (toMatrix X)⁻¹) :
    Matrix.trace (toMatrix C * toMatrix X) - Mixture.dot b y =
      (Fintype.card n : ℝ) * μ := by
  rw [← hd, toMatrix_add, Matrix.add_mul, Matrix.trace_add,
    measurement_adjoint_identity e, hp]
  have hb : Mixture.dot y b = Mixture.dot b y := by
    simp [Mixture.dot, mul_comm]
  rw [hb, hc, Matrix.smul_mul, Matrix.nonsing_inv_mul _
    ((toMatrix X).isUnit_iff_isUnit_det.mp hX.isUnit), Matrix.trace_smul]
  simp [Matrix.trace_one]
  ring

/-- Averaging exact SDP centers preserves the algebraic objective gap, even
when the average is infeasible for the base measurement map. -/
theorem sdp_mixture_objective_gap [DecidableEq n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : I → R → SymmetricMatrix n) (X S : I → SymmetricMatrix n)
    (C : SymmetricMatrix n) (b : R → ℝ) (y : I → R → ℝ)
    (μ : ℝ) (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (hp : ∀ i, measurement (A i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A i) (y i) + S i = C)
    (hX : ∀ i, (toMatrix (X i)).PosDef)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹) :
    Matrix.trace (toMatrix C * toMatrix (symmetricMix w X)) -
      Mixture.dot b (Mixture.mix w y) = (Fintype.card n : ℝ) * μ := by
  rw [← dot_svec e, svec_mix]
  apply Mixture.mixture_objective_gap w hw
  intro i
  rw [dot_svec]
  exact sdp_objective_gap e (A i) (X i) (S i) C b (y i) μ (hp i) (hd i) (hX i) (hc i)

end
end QipmFormal.SDPMixture
