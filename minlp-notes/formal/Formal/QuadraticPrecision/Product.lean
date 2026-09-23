import Formal.QuadraticPrecision.IntervalLower
import Mathlib.Analysis.Convex.Mul

/-! Exact one-sided product construction using a convex positive square and
one discrete hypograph approximation of a negative square. -/
namespace QuadraticPrecision
noncomputable section

def productDomain : Set (Input 2) := {x | ∀ i, x i ∈ Set.Icc 0 1}
def productFunction (x : Input 2) : ℝ := x 0 * x 1

def productSquareMap (p q : ℕ) : LiftPoint 2 p (q+1) →ᵃ[ℝ] LiftPoint 1 p q where
  toFun v := (fun _ => (v.1 0 - v.1 1 + 1)/2, v.2.2.1 0,
    fun i => v.2.2.1 i.succ, v.2.2.2)
  linear := {
    toFun v := (fun _ => (v.1 0 - v.1 1)/2, v.2.2.1 0,
      fun i => v.2.2.1 i.succ, v.2.2.2)
    map_add' := by
      intros
      ext
      all_goals try simp
      all_goals ring
    map_smul' := by
      intros
      ext
      all_goals try simp
      all_goals ring }
  map_vadd' := by
      intros
      ext
      all_goals try simp
      all_goals ring

def productUpperCarrier {p q : ℕ} (L : ConvexIntegerLift 1 p q) :
    Set (LiftPoint 2 p (q+1)) :=
  {v | productSquareMap p q v ∈ L.carrier ∧ v.1 ∈ productDomain ∧
    ((v.1 0 + v.1 1)/2)^2 ≤ v.2.1 + v.2.2.1 0 - (v.1 0-v.1 1+1)/2 + 1/4}

theorem productUpperCarrier_convex {p q : ℕ} (L : ConvexIntegerLift 1 p q) :
    Convex ℝ (productUpperCarrier L) := by
  have hpre := L.convex_carrier.affine_preimage (productSquareMap p q)
  intro v hv v' hv' a b ha hb hab
  refine ⟨hpre hv.1 hv'.1 ha hb hab, ?_, ?_⟩
  · intro i
    exact (convex_Icc (0:ℝ) 1) (hv.2.1 i) (hv'.2.1 i) ha hb hab
  · have hs := (Even.convexOn_pow (𝕜 := ℝ) (show Even 2 from ⟨1, rfl⟩)).2
      (Set.mem_univ ((v.1 0+v.1 1)/2)) (Set.mem_univ ((v'.1 0+v'.1 1)/2)) ha hb hab
    have hh := add_le_add (mul_le_mul_of_nonneg_left hv.2.2 ha)
      (mul_le_mul_of_nonneg_left hv'.2.2 hb)
    simp only [smul_eq_mul] at hs
    change ((a*v.1 0+b*v'.1 0+(a*v.1 1+b*v'.1 1))/2)^2 ≤
      a*v.2.1+b*v'.2.1+(a*v.2.2.1 0+b*v'.2.2.1 0)-
      (a*v.1 0+b*v'.1 0-(a*v.1 1+b*v'.1 1)+1)/2+1/4
    calc
      _ = (a * ((v.1 0+v.1 1)/2) + b * ((v'.1 0+v'.1 1)/2))^2 := by ring
      _ ≤ _ := hs
      _ ≤ _ := hh
      _ = _ := by nlinarith [hab]

def productUpperLift {p q : ℕ} (L : ConvexIntegerLift 1 p q) :
    ConvexIntegerLift 2 p (q+1) := ⟨productUpperCarrier L, productUpperCarrier_convex L⟩

/-- A square hypograph error transfers without loss to the product epigraph. -/
theorem product_epigraph_of_square_hypograph {p : ℕ} {ε : ℝ}
    (h : HasHypographLift unitIntervalDomain squareOne ε p) :
    HasEpigraphLift productDomain productFunction ε p := by
  obtain ⟨q, L, hcontain, hsound⟩ := h
  refine ⟨q+1, productUpperLift L, ?_, ?_⟩
  · intro x hx w hw
    let v : Input 1 := fun _ => (x 0-x 1+1)/2
    have hv : v ∈ unitIntervalDomain := by
      have h0 := hx 0; have h1 := hx 1
      dsimp [unitIntervalDomain, v]; constructor <;> linarith [h0.1, h0.2, h1.1, h1.2]
    obtain ⟨z, a, hz⟩ := hcontain v hv (squareOne v) le_rfl
    refine ⟨z, Fin.cases (squareOne v) a, ?_⟩
    change _ ∈ productUpperCarrier L
    refine ⟨?_, hx, ?_⟩
    · simpa [productSquareMap, v] using hz
    · simp only [Fin.cases_zero]
      dsimp [squareOne, v, productFunction] at *
      nlinarith
  · rintro ⟨x,w⟩ ⟨z, a, hz⟩
    change _ ∈ productUpperCarrier L at hz
    have hs := hsound ((fun _ => (x 0-x 1+1)/2), a 0) ⟨z, (fun i => a i.succ), hz.1⟩
    refine ⟨hz.2.1, ?_⟩
    have hb := hz.2.2
    dsimp [squareOne, productFunction] at hs ⊢
    nlinarith [hs.2]

/-- A square overestimate produces an equal product underestimate on the antidiagonal. -/
theorem productUpperLift_attains {p q : ℕ} (L : ConvexIntegerLift 1 p q)
    {v ε : ℝ} (hv : v ∈ Set.Icc 0 1)
    (h : ((fun _ : Fin 1 => v), v^2+ε) ∈ L.relaxation) :
    (![v,1-v], v*(1-v)-ε) ∈ (productUpperLift L).relaxation := by
  obtain ⟨z,a,hz⟩ := h
  refine ⟨z, Fin.cases (v^2+ε) a, ?_⟩
  change _ ∈ productUpperCarrier L
  refine ⟨?_, ?_, ?_⟩
  · convert hz using 1
    ext i
    all_goals simp [productSquareMap]
    all_goals ring
  · intro i
    fin_cases i
    · exact hv
    · change 0 ≤ 1-v ∧ 1-v ≤ 1
      constructor <;> linarith [hv.1,hv.2]
  · simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Fin.cases_zero]
    ring_nf
    exact le_rfl

/-- Reflecting the second coordinate swaps the product's epigraph and hypograph. -/
def productReflectMap (p q : ℕ) : LiftPoint 2 p q →ᵃ[ℝ] LiftPoint 2 p q where
  toFun v := (![v.1 0, 1-v.1 1], v.1 0-v.2.1, v.2.2.1, v.2.2.2)
  linear := {
    toFun v := (![v.1 0, -v.1 1], v.1 0-v.2.1, v.2.2.1, v.2.2.2)
    map_add' := by
      intros
      ext i
      all_goals simp only [Fin.isValue, Prod.fst_add, Pi.add_apply, neg_add_rev,
        Prod.mk.eta, Prod.mk_add_mk, Matrix.add_cons, Matrix.head_cons,
        Matrix.tail_cons, Matrix.empty_add_empty]
      all_goals try fin_cases i
      all_goals try simp
      all_goals ring
    map_smul' := by
      intros
      ext i
      all_goals simp
      all_goals ring }
  map_vadd' := by
    intros
    ext i
    all_goals simp only [vadd_eq_add, Fin.isValue, Prod.fst_add, Pi.add_apply,
      Prod.mk.eta, LinearMap.coe_mk, AddHom.coe_mk, Prod.mk_add_mk,
      Matrix.add_cons, Matrix.head_cons, Matrix.tail_cons, Matrix.empty_add_empty]
    all_goals try fin_cases i
    all_goals try simp
    all_goals ring

theorem product_reflect_mem {x : Input 2} (hx : x ∈ productDomain) :
    ![x 0, 1-x 1] ∈ productDomain := by
  intro i
  fin_cases i
  · exact hx 0
  · have h := hx 1; constructor <;> simp <;> linarith [h.1,h.2]

theorem product_hypograph_of_epigraph {p : ℕ} {ε : ℝ}
    (h : HasEpigraphLift productDomain productFunction ε p) :
    HasHypographLift productDomain productFunction ε p := by
  obtain ⟨q, L, hcontain, hsound⟩ := h
  let L' : ConvexIntegerLift 2 p q :=
    ⟨productReflectMap p q ⁻¹' L.carrier, L.convex_carrier.affine_preimage _⟩
  refine ⟨q, L', ?_, ?_⟩
  · intro x hx w hw
    have hb : productFunction ![x 0, 1-x 1] ≤ x 0-w := by
      dsimp [productFunction] at hw ⊢
      nlinarith
    obtain ⟨z,a,ha⟩ := hcontain _ (product_reflect_mem hx) _ hb
    exact ⟨z,a,ha⟩
  · rintro ⟨x,w⟩ ⟨z,a,ha⟩
    have hs := hsound (![x 0,1-x 1],x 0-w) ⟨z,a,ha⟩
    refine ⟨?_, ?_⟩
    · intro i
      fin_cases i
      · exact hs.1 0
      · have hb := hs.1 1
        change 0 ≤ 1-x 1 ∧ 1-x 1 ≤ 1 at hb
        change 0 ≤ x 1 ∧ x 1 ≤ 1
        constructor <;> linarith [hb.1,hb.2]
    · dsimp [productFunction] at hs ⊢
      nlinarith [hs.2]


end
end QuadraticPrecision
