import Formal.QuadraticPrecision.ProductExact
import Formal.QuadraticPrecision.UpperBounds
import Formal.QuadraticPrecision.FoldingLift

/-! At any fixed binary count, linear product one-sided lifts attain every
strictly larger error than the optimal convex threshold. -/
namespace QuadraticPrecision
noncomputable section

private def productU : Input 2 →ᵃ[ℝ] ℝ :=
  (1/2:ℝ) • ((LinearMap.proj 0).toAffineMap + (LinearMap.proj 1).toAffineMap)
private def productV : Input 2 →ᵃ[ℝ] ℝ :=
  (1/2:ℝ) • ((LinearMap.proj 0).toAffineMap - (LinearMap.proj 1).toAffineMap +
    AffineMap.const ℝ (Input 2) 1)
private def productAff : Input 2 →ᵃ[ℝ] ℝ :=
  productV - AffineMap.const ℝ (Input 2) (1/4)
private def productP (p : ℕ) : Bool → ℕ | false => 0 | true => p
private def productQ (p L : ℕ) : Bool → ℕ | false => L | true => 2+(p+p)
private def productS (p L : ℕ) : (j : Bool) → BinaryLinearLift 1 (productP p j) (productQ p L j)
  | false => foldingBinaryLift L
  | true => squareBinaryLift p true
private def productY : Bool → Input 2 →ᵃ[ℝ] ℝ | false => productU | true => productV
private def productC : Bool → ℝ | false => 1 | true => -1
private def productBox : LinearSystem (Input 2) := UpperAssembly.boxSystem (fun _ => 0) (fun _ => 1)

private theorem productY_mem {x : Input 2} (hx : x ∈ productDomain) (j : Bool) :
    productY j x ∈ Set.Icc (0:ℝ) 1 := by
  have h0 := hx 0; have h1 := hx 1
  cases j
  · change 0 ≤ (1/2:ℝ)*(x 0+x 1) ∧ (1/2:ℝ)*(x 0+x 1) ≤ 1
    constructor <;> linarith [h0.1,h0.2,h1.1,h1.2]
  · change 0 ≤ (1/2:ℝ)*(x 0-x 1+1) ∧ (1/2:ℝ)*(x 0-x 1+1) ≤ 1
    constructor <;> linarith [h0.1,h0.2,h1.1,h1.2]

/-- A concrete finite row assembly with exactly `p` binaries. -/
theorem product_epigraph_binary_two_depths (p L : ℕ) :
    HasBinaryEpigraphLift productDomain productFunction ((squareWidth p)^2/4+foldError L) p := by
  let B := UpperAssembly.lift productBox (productP p) (productQ p L)
    (productS p L) productY productAff productC true
  have hp : Fintype.card (UpperAssembly.CodeIndex (productP p)) = p := by
    rw [UpperAssembly.code_count]
    simp only [Fintype.sum_bool,productP,Nat.add_zero]
  suffices h : HasBinaryEpigraphLift productDomain productFunction
      ((squareWidth p)^2/4+foldError L) (Fintype.card (UpperAssembly.CodeIndex (productP p))) by
    simpa only [hp] using h
  refine ⟨_, B, ?_, ?_⟩
  · intro x hx w hw
    apply (UpperAssembly.relaxation _ _ _ _ _ _ _ true x w).mpr
    refine ⟨?_, fun j => (productY j x)^2, ?_, ?_, by simp⟩
    · exact (UpperAssembly.boxSystem_feasible _ _ _).mpr hx
    · intro j
      cases j
      · exact (foldingBinaryLift_isEpigraph L).1 _ (productY_mem hx false) _ le_rfl
      · exact (squareBinaryLift_hypograph p).1 _ (productY_mem hx true) _ le_rfl
    · convert hw using 1
      simp [productFunction,productAff,productY,productC,productU,productV]
      ring
  · rintro ⟨x,w⟩ hw
    obtain ⟨hx,t,ht,hw,_⟩ := (UpperAssembly.relaxation _ _ _ _ _ _ _ true x w).mp hw
    refine ⟨(UpperAssembly.boxSystem_feasible _ _ _).mp hx, ?_⟩
    have hpos := ((foldingBinaryLift_isEpigraph L).2 _ (ht false)).2
    have hneg := ((squareBinaryLift_hypograph p).2 _ (ht true)).2
    simp [productY,productU,productV] at hpos hneg
    simp [productAff,productV,productC] at hw
    dsimp [productFunction]
    nlinarith

theorem product_epigraph_binary_slack (p : ℕ) {δ : ℝ} (hδ : 0 < δ) :
    HasBinaryEpigraphLift productDomain productFunction ((1/4:ℝ)^p/4+δ) p := by
  obtain ⟨q,L,hcontains,hsound⟩ := product_epigraph_binary_two_depths p (squarePrecisionCount δ)
  have he := squarePrecisionCount_sufficient hδ
  have heq : (squareWidth p)^2 = (1/4:ℝ)^p := by
    unfold squareWidth
    rw [←pow_mul,mul_comm p 2,pow_mul]
    norm_num
  refine ⟨q,L,hcontains, ?_⟩
  intro v hv
  refine ⟨(hsound v hv).1, ?_⟩
  have hh := (hsound v hv).2
  rw [heq] at hh
  dsimp [foldError] at hh
  linarith

/-- The affine reflection preserves finite linear rows and every binary coordinate. -/
theorem product_binary_hypograph_of_epigraph {p : ℕ} {ε : ℝ}
    (h : HasBinaryEpigraphLift productDomain productFunction ε p) :
    HasBinaryHypographLift productDomain productFunction ε p := by
  obtain ⟨q,L,hcontain,hsound⟩ := h
  let L' : BinaryLinearLift 2 p q := {
    system := L.system.preimage (productReflectMap p q)
    code_bounds := by intro v hv i; exact L.code_bounds _ hv i }
  refine ⟨q,L', ?_, ?_⟩
  · intro x hx w hw
    have hb : productFunction ![x 0,1-x 1] ≤ x 0-w := by
      dsimp [productFunction] at hw ⊢; nlinarith
    obtain ⟨z,hz,a,ha⟩ := hcontain _ (product_reflect_mem hx) _ hb
    exact ⟨z,hz,a,ha⟩
  · rintro ⟨x,w⟩ ⟨z,hz,a,ha⟩
    have hs := hsound (![x 0,1-x 1],x 0-w) ⟨z,hz,a,ha⟩
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

theorem product_hypograph_binary_slack (p : ℕ) {δ : ℝ} (hδ : 0 < δ) :
    HasBinaryHypographLift productDomain productFunction ((1/4:ℝ)^p/4+δ) p :=
  product_binary_hypograph_of_epigraph (product_epigraph_binary_slack p hδ)

end
end QuadraticPrecision
