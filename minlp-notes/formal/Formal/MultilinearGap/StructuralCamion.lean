import Formal.MultilinearGap.StructuralTreewidthGraph
import Formal.MultilinearGap.StructuralTreewidthDecomposition
import Formal.MultilinearGap.StructuralTreewidthTU
import Formal.MultilinearGap.StructuralGHParity

/-!
# Incidence-cycle restrictions and the signing criterion for TU

Injective graph homomorphisms preserve simple cycles and their factor counts.
Consequently a good factor coloring restricts to every matrix submatrix selected
by distinct rows and columns.

The column form of the Ghouila-Houri signing criterion implies total
unimodularity, proved here by cofactor induction. The remaining graph step
is to obtain those signs from the cycle parity condition; it is not assumed
or asserted by the determinant argument.
-/

namespace MultilinearGap.TreewidthGraph

variable {V W : Type*} {G : SimpleGraph V} {H : SimpleGraph W}

/-- Mapping a walk preserves factor parity when the factor marking is pulled
back along the map. -/
theorem cycleParity_map (f : G →g H) (factor : W → Bool) {u : V}
    (p : G.Walk u u) :
    cycleParity factor (p.map f) = cycleParity (factor ∘ f) p := by
  simp [cycleParity, SimpleGraph.Walk.support_map, ← List.map_tail,
    List.map_map, Function.comp_def, factorWeight]
  rfl

/-- A monochromatic walk remains monochromatic in the target graph. -/
theorem monochromatic_map (f : G →g H) (factor color : W → Bool)
    {u v : V} (p : G.Walk u v) (c : Bool) :
    Monochromatic factor color c (p.map f) ↔
      Monochromatic (factor ∘ f) (color ∘ f) c p := by
  simp [Monochromatic, SimpleGraph.Walk.support_map]

/-- A good coloring pulls back through an injective graph homomorphism. The
injectivity matters: a simple cycle must remain a simple cycle. -/
theorem good_of_injective_hom (f : G →g H) (hf : Function.Injective f)
    (factor color : W → Bool) (h : Good factor color H) :
    Good (factor ∘ f) (color ∘ f) G := by
  intro u p hp c hc
  rw [← cycleParity_map f factor p]
  exact h (f u) (p.map f) (hp.map hf) c ((monochromatic_map f factor color p c).mpr hc)

end MultilinearGap.TreewidthGraph

namespace MultilinearGap.StructuralTreewidth

variable {I J I' J' : Type*}

/-- Selecting rows and columns gives the natural homomorphism of incidence
graphs, even before requiring that the selections be injective. -/
def incidenceSubmatrixHom (incident : I → J → Prop) (f : I' → I) (g : J' → J) :
    incidenceGraph (fun i j => incident (f i) (g j)) →g incidenceGraph incident where
  toFun := Sum.map f g
  map_rel' := by
    intro v w h
    cases v <;> cases w <;> exact h

theorem incidenceSubmatrixHom_injective (incident : I → J → Prop)
    {f : I' → I} {g : J' → J} (hf : Function.Injective f) (hg : Function.Injective g) :
    Function.Injective (incidenceSubmatrixHom incident f g) :=
  Sum.map_injective.mpr ⟨hf, hg⟩

/-- Every injective row and column restriction inherits the good coloring of
the original incidence graph. Factors occupy the right side of the sum. -/
theorem incidence_good_submatrix (incident : I → J → Prop)
    {f : I' → I} {g : J' → J} (hf : Function.Injective f) (hg : Function.Injective g)
    (color : I ⊕ J → Bool)
    (h : TreewidthGraph.Good (Sum.elim (fun _ => false) (fun _ => true)) color
      (incidenceGraph incident)) :
    TreewidthGraph.Good (Sum.elim (fun _ => false) (fun _ => true))
      (color ∘ Sum.map f g) (incidenceGraph (fun i j => incident (f i) (g j))) := by
  have heq : (Sum.elim (fun _ : I => false) (fun _ : J => true)) ∘
      (incidenceSubmatrixHom incident f g) =
      Sum.elim (fun _ : I' => false) (fun _ : J' => true) := by
    funext x
    cases x <;> rfl
  have hh := TreewidthGraph.good_of_injective_hom (incidenceSubmatrixHom incident f g)
    (incidenceSubmatrixHom_injective incident hf hg) _ color h
  rw [heq] at hh
  exact hh

end MultilinearGap.StructuralTreewidth

namespace MultilinearGap

open Matrix

/-- The column form of the Ghouila-Houri signing condition: every finite set of
distinct columns admits signs whose row sums are zero or a unit. -/
def ColumnSigning {m n : Type*} (A : Matrix m n ℤ) : Prop :=
  ∀ (k : ℕ) (g : Fin k → n), Function.Injective g →
    ∃ s : Fin k → ℤ, (∀ j, s j = 1 ∨ s j = -1) ∧
      ∀ i, (∑ j, A i (g j) * s j) ∈ Set.range SignType.cast

/-- The signing condition passes to submatrices with distinct selected columns. -/
theorem ColumnSigning.submatrix {m n m' n' : Type*} {A : Matrix m n ℤ}
    (h : ColumnSigning A) (f : m' → m) (g : n' → n) (hg : Function.Injective g) :
    ColumnSigning (A.submatrix f g) := by
  intro k a ha
  obtain ⟨s, hs, hb⟩ := h k (g ∘ a) (hg.comp ha)
  exact ⟨s, hs, fun i => hb (f i)⟩

/-- The signing condition can be applied to the support of a prescribed
vector, leaving all other coordinates zero. -/
theorem ColumnSigning.support {m n : Type*} [Fintype n] {A : Matrix m n ℤ}
    (h : ColumnSigning A) (u : n → ℤ) :
    ∃ v : n → ℤ, (∀ j, u j = 0 → v j = 0) ∧
      (∀ j, u j ≠ 0 → v j = 1 ∨ v j = -1) ∧
      ∀ i, (A *ᵥ v) i ∈ Set.range SignType.cast := by
  classical
  let S : Finset n := Finset.univ.filter fun j => u j ≠ 0
  let e : Fin (Fintype.card S) ≃ S := (Fintype.equivFin S).symm
  obtain ⟨s, hs, hb⟩ := h _ (fun j => (e j).val) (Subtype.val_injective.comp e.injective)
  let v : n → ℤ := fun j => if hj : j ∈ S then s (e.symm ⟨j, hj⟩) else 0
  refine ⟨v, ?_, ?_, ?_⟩
  · intro j hj
    simp [v, S, hj]
  · intro j hj
    have hjS : j ∈ S := by simp [S, hj]
    simpa [v, hjS] using hs (e.symm ⟨j, hjS⟩)
  · intro i
    have heq : (A *ᵥ v) i = ∑ j : S, A i j.val * s (e.symm j) := by
      change (∑ j, A i j * v j) = _
      calc
        _ = ∑ j ∈ S, A i j * v j := by
          symm
          apply Finset.sum_subset (Finset.subset_univ S)
          intro j _ hj
          simp [v, hj]
        _ = ∑ j : S, A i j.val * v j.val :=
          Finset.sum_subtype S (fun _ => Iff.rfl) _
        _ = _ := by
          apply Finset.sum_congr rfl
          intro j _
          simp [v, j.property]
    rw [heq, ← e.sum_comp (fun j => A i j.val * s (e.symm j))]
    simpa using hb i

/-- The signing criterion forces the determinant of each square integer
matrix to be zero or a unit. Cofactor induction supplies a zero/unit vector;
its signing agrees modulo two and isolates one row of the matrix product. -/
theorem ColumnSigning.det : ∀ (k : ℕ) (A : Matrix (Fin k) (Fin k) ℤ),
    ColumnSigning A → A.det ∈ Set.range SignType.cast := by
  intro k
  induction k with
  | zero => intro A _; exact ⟨1, by simp⟩
  | succ k ih =>
    intro A hA
    by_cases hd : A.det = 0
    · exact ⟨0, by simpa using hd.symm⟩
    let u : Fin (k + 1) → ℤ := fun j => A.adjugate j 0
    have hu (j : Fin (k + 1)) : u j ∈ Set.range SignType.cast := by
      dsimp [u]
      rw [Matrix.adjugate_fin_succ_eq_det_submatrix]
      change _ ∈ MonoidHom.mrange SignType.castHom.toMonoidHom
      apply mul_mem
      · exact pow_mem (show (-1 : ℤ) ∈ MonoidHom.mrange SignType.castHom.toMonoidHom
          from ⟨-1, by simp⟩) _
      · exact ih _ (hA.submatrix _ _ Fin.succAbove_right_injective)
    have hAu : A *ᵥ u = Pi.single 0 A.det := by
      ext i
      change (A * A.adjugate) i 0 = _
      rw [Matrix.mul_adjugate]
      simp [Matrix.smul_apply, Matrix.one_apply, Pi.single_apply]
    obtain ⟨j, hj⟩ : ∃ j, u j ≠ 0 := by
      by_contra hh
      push Not at hh
      have hz : u = 0 := funext hh
      have he := congrFun hAu 0
      simp [hz] at he
      exact hd he.symm
    obtain ⟨v, hvzero, hvunit, hvsum⟩ := hA.support u
    let w := A *ᵥ v
    have hwzero (i : Fin (k + 1)) (hi : i ≠ 0) : w i = 0 := by
      apply sign_int_cast_zero (hvsum i)
      have hp := mulVec_sign_cast_zmod_two A hu hvzero hvunit i
      rw [hAu] at hp
      simpa [Pi.single_apply, hi, Ne.symm hi] using hp.symm
    have hw : w = Pi.single 0 (w 0) := by
      ext i
      by_cases hi : i = 0
      · subst i; simp
      · simp [hi, hwzero i hi]
    have hdv : A.det • v = (w 0) • u := by
      calc
        A.det • v = A.adjugate *ᵥ (A *ᵥ v) := by
          rw [Matrix.mulVec_mulVec, Matrix.adjugate_mul,
            Matrix.smul_mulVec, Matrix.one_mulVec]
        _ = A.adjugate *ᵥ w := rfl
        _ = (w 0) • u := by
          rw [hw]
          ext i
          simp [Matrix.mulVec, dotProduct, Pi.single_apply, u, mul_comm]
    have he : A.det * v j = w 0 * u j := congrFun hdv j
    exact sign_of_scaled_units he (hvunit j hj) (hu j) (hvsum 0)

/-- Ghouila-Houri sufficiency, in column form, with no finite ambient-index
assumption. Every finite square submatrix inherits the signing condition. -/
theorem ColumnSigning.totallyUnimodular {m n : Type*} {A : Matrix m n ℤ}
    (h : ColumnSigning A) : A.IsTotallyUnimodular := by
  intro k f g _ hg
  exact ColumnSigning.det k _ (h.submatrix f g hg)

end MultilinearGap
