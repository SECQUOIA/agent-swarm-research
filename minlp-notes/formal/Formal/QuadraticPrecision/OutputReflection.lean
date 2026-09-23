import Formal.QuadraticPrecision.BinaryModel

/-! Reversing a scalar output converts complete epigraphs to complete
hypographs without changing integer dimension or inequality count. -/
namespace QuadraticPrecision
noncomputable section

def outputReflection (n p q : ℕ) : LiftPoint n p q →ₗ[ℝ] LiftPoint n p q where
  toFun v := (v.1, -v.2.1, v.2.2.1, v.2.2.2)
  map_add' _ _ := by ext <;> simp [add_comm]
  map_smul' _ _ := by ext <;> simp

def BinaryLinearLift.reflect {n p q : ℕ} (L : BinaryLinearLift n p q) :
    BinaryLinearLift n p q where
  system := L.system.preimage (outputReflection n p q).toAffineMap
  code_bounds v hv i := L.code_bounds (outputReflection n p q v) hv i

theorem BinaryLinearLift.reflect_relaxation {n p q : ℕ} (L : BinaryLinearLift n p q)
    (x : Input n) (w : ℝ) :
    (x,w) ∈ L.reflect.relaxation ↔ (x,-w) ∈ L.relaxation := Iff.rfl

theorem BinaryLinearLift.reflect_rowCount {n p q : ℕ} (L : BinaryLinearLift n p q) :
    L.reflect.system.rowCount = L.system.rowCount := rfl

theorem HasBinaryEpigraphLift.neg {n p : ℕ} {D : Set (Input n)}
    {f : Input n → ℝ} {ε : ℝ} (h : HasBinaryEpigraphLift D f ε p) :
    HasBinaryHypographLift D (fun x => -f x) ε p := by
  obtain ⟨q,L,hc,hs⟩ := h
  refine ⟨q,L.reflect, ?_, ?_⟩
  · intro x hx w hw
    apply (L.reflect_relaxation x w).mpr
    exact hc x hx (-w) (by linarith)
  · intro v hv
    have h := hs (v.1,-v.2) ((L.reflect_relaxation v.1 v.2).mp hv)
    exact ⟨h.1, by dsimp at h ⊢; linarith [h.2]⟩

theorem HasBinaryHypographLift.neg {n p : ℕ} {D : Set (Input n)}
    {f : Input n → ℝ} {ε : ℝ} (h : HasBinaryHypographLift D f ε p) :
    HasBinaryEpigraphLift D (fun x => -f x) ε p := by
  obtain ⟨q,L,hc,hs⟩ := h
  refine ⟨q,L.reflect, ?_, ?_⟩
  · intro x hx w hw
    apply (L.reflect_relaxation x w).mpr
    exact hc x hx (-w) (by linarith)
  · intro v hv
    have h := hs (v.1,-v.2) ((L.reflect_relaxation v.1 v.2).mp hv)
    exact ⟨h.1, by dsimp at h ⊢; linarith [h.2]⟩

def ConvexIntegerLift.reflect {n p q : ℕ} (L : ConvexIntegerLift n p q) :
    ConvexIntegerLift n p q where
  carrier := outputReflection n p q ⁻¹' L.carrier
  convex_carrier := L.convex_carrier.linear_preimage (outputReflection n p q)

theorem ConvexIntegerLift.reflect_relaxation {n p q : ℕ} (L : ConvexIntegerLift n p q)
    (x : Input n) (w : ℝ) :
    (x,w) ∈ L.reflect.relaxation ↔ (x,-w) ∈ L.relaxation := Iff.rfl

theorem HasEpigraphLift.neg {n p : ℕ} {D : Set (Input n)}
    {f : Input n → ℝ} {ε : ℝ} (h : HasEpigraphLift D f ε p) :
    HasHypographLift D (fun x => -f x) ε p := by
  obtain ⟨q,L,hc,hs⟩ := h
  refine ⟨q,L.reflect, ?_, ?_⟩
  · intro x hx w hw
    apply (L.reflect_relaxation x w).mpr
    exact hc x hx (-w) (by linarith)
  · intro v hv
    have h := hs (v.1,-v.2) ((L.reflect_relaxation v.1 v.2).mp hv)
    exact ⟨h.1, by dsimp at h ⊢; linarith [h.2]⟩

theorem HasHypographLift.neg {n p : ℕ} {D : Set (Input n)}
    {f : Input n → ℝ} {ε : ℝ} (h : HasHypographLift D f ε p) :
    HasEpigraphLift D (fun x => -f x) ε p := by
  obtain ⟨q,L,hc,hs⟩ := h
  refine ⟨q,L.reflect, ?_, ?_⟩
  · intro x hx w hw
    apply (L.reflect_relaxation x w).mpr
    exact hc x hx (-w) (by linarith)
  · intro v hv
    have h := hs (v.1,-v.2) ((L.reflect_relaxation v.1 v.2).mp hv)
    exact ⟨h.1, by dsimp at h ⊢; linarith [h.2]⟩

end
end QuadraticPrecision
