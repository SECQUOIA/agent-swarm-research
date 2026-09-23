import Formal.QuadraticPrecision.Parity
import Mathlib.LinearAlgebra.AffineSpace.AffineMap
namespace QuadraticPrecision
theorem affineMap_mix {n m : ℕ} (A : Input m →ᵃ[ℝ] Input n)
    (x y : Input m) {a b : ℝ} (hab : a + b = 1) :
    A (a • x+b • y) = a • A x+b • A y := by
  have hd (z) : A z = A.linear z + A 0 := congrFun A.decomp z
  rw [hd, hd x, hd y, map_add, map_smul, map_smul, smul_add, smul_add]
  have h : a • A 0+b • A 0 = A 0 := by rw [← add_smul, hab, one_smul]
  calc
    _ = a • A.linear x + b • A.linear y + (a • A 0+b • A 0) := by rw [h]
    _ = _ := by abel
namespace ConvexIntegerLift
noncomputable def pullback {n m p q : ℕ} (L : ConvexIntegerLift n p q)
    (A : Input m →ᵃ[ℝ] Input n) (K : Set (Input m)) (hK : Convex ℝ K) :
    ConvexIntegerLift m p q where
  carrier := {v | v.1 ∈ K ∧ (A v.1, v.2) ∈ L.carrier}
  convex_carrier := by
    intro v hv w hw a b ha hb hab
    refine ⟨hK hv.1 hw.1 ha hb hab, ?_⟩
    have hh := L.convex_carrier hv.2 hw.2 ha hb hab
    change (A (a • v.1 + b • w.1), a • v.2 + b • w.2) ∈ L.carrier
    rw [affineMap_mix A _ _ hab]
    simpa only [Prod.fst_add, Prod.fst_smul, Prod.snd_add, Prod.snd_smul,
      affineMap_mix A _ _ hab, Prod.smul_mk, Prod.mk_add_mk] using hh
@[simp] theorem pullback_relaxation {n m p q : ℕ} (L : ConvexIntegerLift n p q)
    (A : Input m →ᵃ[ℝ] Input n) (K : Set (Input m)) (hK : Convex ℝ K)
    (v : Input m × ℝ) :
    v ∈ (L.pullback A K hK).relaxation ↔ v.1 ∈ K ∧ (A v.1,v.2) ∈ L.relaxation := by
  constructor
  · rintro ⟨z,u,hK,hu⟩; exact ⟨hK,z,u,hu⟩
  · rintro ⟨hK,z,u,hu⟩; exact ⟨z,u,hK,hu⟩
end ConvexIntegerLift

theorem HasGraphLift.pullback {n m p : ℕ} {D : Set (Input n)} {f : Input n → ℝ}
    {ε : ℝ} (h : HasGraphLift D f ε p) (A : Input m →ᵃ[ℝ] Input n)
    (K : Set (Input m)) (hK : Convex ℝ K) (hKD : ∀ x ∈ K, A x ∈ D) :
    HasGraphLift K (f ∘ A) ε p := by
  obtain ⟨q,L,hL⟩ := h
  refine ⟨q,L.pullback A K hK, ?_, ?_⟩
  · intro x hx
    exact (L.pullback_relaxation A K hK _).mpr ⟨hx,hL.1 _ (hKD x hx)⟩
  · intro v hv
    obtain ⟨hx,hv⟩ := (L.pullback_relaxation A K hK _).mp hv
    exact ⟨hx,(hL.2 _ hv).2⟩

theorem HasEpigraphLift.pullback {n m p : ℕ} {D : Set (Input n)} {f : Input n → ℝ}
    {ε : ℝ} (h : HasEpigraphLift D f ε p) (A : Input m →ᵃ[ℝ] Input n)
    (K : Set (Input m)) (hK : Convex ℝ K) (hKD : ∀ x ∈ K, A x ∈ D) :
    HasEpigraphLift K (f ∘ A) ε p := by
  obtain ⟨q,L,hL⟩ := h
  refine ⟨q,L.pullback A K hK, ?_, ?_⟩
  · intro x hx w hw
    exact (L.pullback_relaxation A K hK _).mpr ⟨hx,hL.1 _ (hKD x hx) w hw⟩
  · intro v hv
    obtain ⟨hx,hv⟩ := (L.pullback_relaxation A K hK _).mp hv
    exact ⟨hx,(hL.2 _ hv).2⟩

theorem HasHypographLift.pullback {n m p : ℕ} {D : Set (Input n)} {f : Input n → ℝ}
    {ε : ℝ} (h : HasHypographLift D f ε p) (A : Input m →ᵃ[ℝ] Input n)
    (K : Set (Input m)) (hK : Convex ℝ K) (hKD : ∀ x ∈ K, A x ∈ D) :
    HasHypographLift K (f ∘ A) ε p := by
  obtain ⟨q,L,hL⟩ := h
  refine ⟨q,L.pullback A K hK, ?_, ?_⟩
  · intro x hx w hw
    exact (L.pullback_relaxation A K hK _).mpr ⟨hx,hL.1 _ (hKD x hx) w hw⟩
  · intro v hv
    obtain ⟨hx,hv⟩ := (L.pullback_relaxation A K hK _).mp hv
    exact ⟨hx,(hL.2 _ hv).2⟩
end QuadraticPrecision
