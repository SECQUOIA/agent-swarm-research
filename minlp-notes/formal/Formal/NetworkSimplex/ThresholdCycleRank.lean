import Formal.NetworkSimplex.ProfileHull

/-! The cycle-space dimension of the actual chain incidence map. -/
namespace NetworkSimplex.Chain
noncomputable section

/-- A conserved zero-demand flow is determined by its b-arcs and bypass. -/
def kernelProjection (L : ℕ) : LinearMap.ker (incidence L) →ₗ[ℝ] ((Fin L → ℝ) × ℝ) where
  toFun f := (fun i => f.val (b i), f.val bypass)
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem kernelProjection_bijective (L : ℕ) : Function.Bijective (kernelProjection L) := by
  constructor
  · intro f g he
    have hf := (conservation_iff L f.val 0).mp (by simp)
    have hg := (conservation_iff L g.val 0).mp (by simp)
    have hb : ∀ i, f.val (b i) = g.val (b i) := fun i => congrFun (congrArg Prod.fst he) i
    have hh : f.val bypass = g.val bypass := congrArg Prod.snd he
    apply Subtype.ext
    funext e
    rcases e with ⟨i, flag⟩ | z
    · cases flag
      · change f.val (a i) = g.val (a i)
        linarith [hf i, hg i, hb i]
      · exact hb i
    · exact hh
  · rintro ⟨g, h⟩
    let f := pack (fun i => -g i - h) g h
    have hf : incidence L f = 0 := by
      have he := (conservation_iff L f 0).mpr (by intro i; dsimp [f]; ring)
      simpa using he
    exact ⟨⟨f, hf⟩, rfl⟩

def kernelCoordinates (L : ℕ) : LinearMap.ker (incidence L) ≃ₗ[ℝ] ((Fin L → ℝ) × ℝ) :=
  LinearEquiv.ofBijective (kernelProjection L) (kernelProjection_bijective L)

/-- Thus the cycle rank is a kernel dimension, not only an edge-minus-vertex count. -/
theorem cycle_rank (L : ℕ) : Module.finrank ℝ (LinearMap.ker (incidence L)) = L + 1 := by
  rw [(kernelCoordinates L).finrank_eq]
  simp

theorem four_cycle_rank : Module.finrank ℝ (LinearMap.ker (incidence 4)) = 5 := cycle_rank 4

end
end NetworkSimplex.Chain
