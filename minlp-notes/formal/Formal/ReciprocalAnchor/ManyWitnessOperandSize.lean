import Formal.ReciprocalAnchor.ManyRationalWitness
import Formal.ReciprocalAnchor.ManyRationalMix

/-! Actual intermediate rational sizes in threshold selection, interpolation, and mixing. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

variable {ι : Type*} [Fintype ι]

/-- The cached strict-tail mass and equal-location mass determine threshold rounding. -/
def thresholdTrace (p x : ι → ℚ) (q s : ℚ) (i : ι) : List ℚ :=
  let A := ∑ k, if s < x k then p k else 0
  let D := ∑ k, if x k = s then p k else 0
  [0, 1, q, A, D, q - A, (q - A) / D, thresholdSelection p x q s i]

theorem thresholdTrace_bits (p x : ι → ℚ) (q s : ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hq : RationalBits q B) (i : ι) :
    ∀ v ∈ thresholdTrace p x q s i, RationalBits v (tailBits (Fintype.card ι) B) := by
  classical
  have hA := rational_tail_partial_bits p hp (rationalBits_pos hq) Finset.univ
    (fun k => s < x k)
  have hD := rational_tail_partial_bits p hp (rationalBits_pos hq) Finset.univ
    (fun k => x k = s)
  have hnum := rationalBits_sub hq hA
  have hr := rationalBits_div hnum hD
  simp only [thresholdTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono rationalBits_zero (by unfold tailBits; omega),
    rationalBits_mono rationalBits_one (by unfold tailBits; omega),
    rationalBits_mono hq (by unfold tailBits; omega),
    rationalBits_mono hA (by unfold tailBits; omega),
    rationalBits_mono hD (by unfold tailBits; omega),
    rationalBits_mono hnum (by unfold tailBits; omega),
    rationalBits_mono hr (by unfold tailBits; omega), thresholdSelection_bits p x q s hp hq i⟩

/-- Intermediates of the actual interpolation formula, including the equal-moment branch. -/
def interpolationTrace (p x θ₀ θ₁ : ι → ℚ) (w : ℚ) (i : ι) : List ℚ :=
  let v₀ := selectionMoment p x θ₀
  let v₁ := selectionMoment p x θ₁
  let r := (w - v₀) / (v₁ - v₀)
  [1, w, θ₀ i, θ₁ i, v₀, v₁, w - v₀, v₁ - v₀, r, 1 - r,
    (1 - r) * θ₀ i, r * θ₁ i, (1 - r) * θ₀ i + r * θ₁ i,
    interpolatedSelection p x θ₀ θ₁ w i]

theorem interpolationTrace_bits (p x θ₀ θ₁ : ι → ℚ) (w : ℚ) {B C : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hx : ∀ i, RationalBits (x i) B)
    (h₀ : ∀ i, RationalBits (θ₀ i) C) (h₁ : ∀ i, RationalBits (θ₁ i) C)
    (hw : RationalBits w B) (i : ι) :
    ∀ v ∈ interpolationTrace p x θ₀ θ₁ w i,
      RationalBits v (interpolationBits (Fintype.card ι) B C) := by
  have hv₀ := selectionMoment_bits p x θ₀ hp hx h₀
  have hv₁ := selectionMoment_bits p x θ₁ hp hx h₁
  have hn := rationalBits_sub hw hv₀
  have hd := rationalBits_sub hv₁ hv₀
  have hr := rationalBits_div hn hd
  have hc := rationalBits_sub rationalBits_one hr
  have hp₀ := rationalBits_mul hc (h₀ i)
  have hp₁ := rationalBits_mul hr (h₁ i)
  simp only [interpolationTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono rationalBits_one (by unfold interpolationBits; omega),
    rationalBits_mono hw (by unfold interpolationBits; omega),
    rationalBits_mono (h₀ i) (by unfold interpolationBits; omega),
    rationalBits_mono (h₁ i) (by unfold interpolationBits; omega),
    rationalBits_mono hv₀ (by unfold interpolationBits; omega),
    rationalBits_mono hv₁ (by unfold interpolationBits; omega),
    rationalBits_mono hn (by unfold interpolationBits; omega),
    rationalBits_mono hd (by unfold interpolationBits; omega),
    rationalBits_mono hr (by unfold interpolationBits; omega),
    rationalBits_mono hc (by unfold interpolationBits; omega),
    rationalBits_mono hp₀ (by unfold interpolationBits; omega),
    rationalBits_mono hp₁ (by unfold interpolationBits; omega),
    rationalBits_mono (rationalBits_add hp₀ hp₁) (by unfold interpolationBits; omega),
    interpolatedSelection_bits p x θ₀ θ₁ w hp hx h₀ h₁ hw i⟩

/-- The two extremal selector coordinates have this bound independently of feasibility. -/
theorem extremal_selector_bits (p x : ι → ℚ) (q s₀ s₁ : ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hq : RationalBits q B) :
    (∀ i, RationalBits (1 - thresholdSelection p x (1 - q) s₀ i)
      (tailBits (Fintype.card ι) (B + 2) + 2)) ∧
    (∀ i, RationalBits (thresholdSelection p x q s₁ i)
      (tailBits (Fintype.card ι) (B + 2) + 2)) := by
  have hp' := fun i => rationalBits_mono (hp i) (by omega : B ≤ B + 2)
  have hq' := rationalBits_mono hq (by omega : B ≤ B + 2)
  have hqc : RationalBits (1 - q) (B + 2) := by
    convert rationalBits_sub rationalBits_one hq using 1; omega
  constructor
  · intro i
    convert rationalBits_sub rationalBits_one
      (thresholdSelection_bits p x (1 - q) s₀ hp' hqc i) using 1
    omega
  · intro i
    exact rationalBits_mono (thresholdSelection_bits p x q s₁ hp' hq' i) (by omega)

/-- A polynomial width for all witness-selector operands and returned graph coordinates. -/
def witnessOperandBits (N B : ℕ) : ℕ := witnessBits N B + 4 * B + 10

theorem witnessOperandBits_lower (N B : ℕ) :
    B + 2 ≤ witnessOperandBits N B ∧
    tailBits N (B + 2) + 2 ≤ witnessOperandBits N B ∧
    momentBits N (B + 2) (tailBits N (B + 2) + 2) ≤ witnessOperandBits N B := by
  unfold witnessOperandBits witnessBits interpolationBits
  omega

/-- Every actual threshold-search partial sum is polynomially bounded. -/
theorem witness_tail_operand_bits (p : ι → ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hB : 0 < B) (S : Finset ι)
    (f : ι → Prop) [DecidablePred f] :
    RationalBits (∑ i ∈ S, if f i then p i else 0)
      (witnessOperandBits (Fintype.card ι) B) := by
  apply rationalBits_mono (rational_tail_partial_bits p
    (fun i => rationalBits_mono (hp i) (by omega : B ≤ B + 2)) (by omega) S f)
  have := (witnessOperandBits_lower (Fintype.card ι) B).2.1
  unfold tailBits at this
  omega

/-- Both cached threshold-ratio computations fit the witness width. -/
theorem witness_threshold_operand_bits (p x : ι → ℚ) (q s : ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hq : RationalBits q B) (i : ι) :
    (∀ v ∈ thresholdTrace p x q s i, RationalBits v (witnessOperandBits (Fintype.card ι) B)) ∧
    (∀ v ∈ thresholdTrace p x (1 - q) s i,
      RationalBits v (witnessOperandBits (Fintype.card ι) B)) := by
  have hp' := fun j => rationalBits_mono (hp j) (by omega : B ≤ B + 2)
  have hq' := rationalBits_mono hq (by omega : B ≤ B + 2)
  have hqc : RationalBits (1 - q) (B + 2) := by
    convert rationalBits_sub rationalBits_one hq using 1; omega
  have hle : tailBits (Fintype.card ι) (B + 2) ≤ witnessOperandBits (Fintype.card ι) B := by
    have := (witnessOperandBits_lower (Fintype.card ι) B).2.1
    omega
  exact ⟨fun v hv => rationalBits_mono (thresholdTrace_bits p x q s hp' hq' i v hv) hle,
    fun v hv => rationalBits_mono (thresholdTrace_bits p x (1 - q) s hp' hqc i v hv) hle⟩

/-- Moment accumulation, including every partial sum, uses the extremal-coordinate bound. -/
theorem witness_moment_operand_bits (p x θ : ι → ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hx : ∀ i, RationalBits (x i) B)
    (hθ : ∀ i, RationalBits (θ i) (tailBits (Fintype.card ι) (B + 2) + 2))
    (S : Finset ι) :
    RationalBits (∑ i ∈ S, p i * x i * θ i)
      (witnessOperandBits (Fintype.card ι) B) := by
  apply rationalBits_mono (rational_moment_partial_bits p x θ
    (fun i => rationalBits_mono (hp i) (by omega : B ≤ B + 2))
    (fun i => rationalBits_mono (hx i) (by omega : B ≤ B + 2)) hθ S)
  exact (witnessOperandBits_lower (Fintype.card ι) B).2.2

/-- All actual interpolation operations have bounded width, even when the moments coincide. -/
theorem witness_interpolation_operand_bits (p x : ι → ℚ) (q w s₀ s₁ : ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hx : ∀ i, RationalBits (x i) B)
    (hq : RationalBits q B) (hw : RationalBits w B) (i : ι) :
    ∀ v ∈ interpolationTrace p x (fun j => 1 - thresholdSelection p x (1 - q) s₀ j)
      (thresholdSelection p x q s₁) w i,
      RationalBits v (witnessOperandBits (Fintype.card ι) B) := by
  obtain ⟨h₀, h₁⟩ := extremal_selector_bits p x q s₀ s₁ hp hq
  intro v hv
  apply rationalBits_mono (interpolationTrace_bits p x _ _ w
    (fun j => rationalBits_mono (hp j) (by omega : B ≤ B + 2))
    (fun j => rationalBits_mono (hx j) (by omega : B ≤ B + 2)) h₀ h₁
    (rationalBits_mono hw (by omega : B ≤ B + 2)) i v hv)
  unfold witnessOperandBits witnessBits
  omega

/-- Exact rational selectors themselves need no feasibility assumptions for their size bound. -/
theorem witness_selector_bits (p x : ι → ℚ) (q w s₀ s₁ : ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hx : ∀ i, RationalBits (x i) B)
    (hq : RationalBits q B) (hw : RationalBits w B) (i : ι) :
    RationalBits (interpolatedSelection p x (fun j => 1 - thresholdSelection p x (1 - q) s₀ j)
      (thresholdSelection p x q s₁) w i) (witnessBits (Fintype.card ι) B) := by
  obtain ⟨h₀, h₁⟩ := extremal_selector_bits p x q s₀ s₁ hp hq
  exact interpolatedSelection_bits p x _ _ w
    (fun j => rationalBits_mono (hp j) (by omega : B ≤ B + 2))
    (fun j => rationalBits_mono (hx j) (by omega : B ≤ B + 2)) h₀ h₁
    (rationalBits_mono hw (by omega : B ≤ B + 2)) i

/-- Returned reciprocal and product coordinates have the same polynomial width. -/
theorem witness_graph_coordinate_bits {N B : ℕ} {x θ p : ℚ}
    (hx : RationalBits x B) (hp : RationalBits p B) (hθ : RationalBits θ (witnessBits N B)) :
    RationalBits (1 / x) (witnessOperandBits N B) ∧
    RationalBits (x * θ) (witnessOperandBits N B) ∧
    RationalBits (p * (x * θ)) (witnessOperandBits N B) := by
  unfold witnessOperandBits
  exact ⟨rationalBits_mono (rationalBits_div rationalBits_one hx) (by omega),
    rationalBits_mono (rationalBits_mul hx hθ) (by omega),
    rationalBits_mono (rationalBits_mul hp (rationalBits_mul hx hθ)) (by omega)⟩

/-- Individual products in moment accumulation also fit the common width. -/
theorem witness_moment_product_bits {N B : ℕ} {p x θ : ℚ}
    (hp : RationalBits p B) (hx : RationalBits x B)
    (hθ : RationalBits θ (tailBits N (B + 2) + 2)) :
    RationalBits (p * x) (witnessOperandBits N B) ∧
    RationalBits (p * x * θ) (witnessOperandBits N B) := by
  unfold witnessOperandBits witnessBits interpolationBits
  exact ⟨rationalBits_mono (rationalBits_mul hp hx) (by omega),
    rationalBits_mono (rationalBits_mul (rationalBits_mul hp hx) hθ) (by omega)⟩

theorem witnessOperandBits_mono {N M B : ℕ} (h : N ≤ M) :
    witnessOperandBits N B ≤ witnessOperandBits M B := by
  unfold witnessOperandBits witnessBits interpolationBits momentBits tailBits
  gcongr

theorem input_le_witnessOperandBits (N B : ℕ) : B ≤ witnessOperandBits N B := by
  have := (witnessOperandBits_lower N B).1
  omega

/-- Every rational intermediate in the actual secant and endpoint mixing formulas. -/
def mixingTrace (a b m t T p : ℚ) : List ℚ :=
  let U := rationalSecant a b m
  let r := rationalMixWeight a b m t T
  [0, 1, a, b, m, t, T, p, a + b, a + b - m, a * b, U,
    t - T, U - T, r, 1 - r, b - m, b - a, m - a,
    (b - m) / (b - a), (m - a) / (b - a),
    (1 - r) * p, r * ((b - m) / (b - a)), r * ((m - a) / (b - a))]

theorem mixingTrace_bits {a b m t T p : ℚ} {B : ℕ}
    (ha : RationalBits a B) (hb : RationalBits b B) (hm : RationalBits m B)
    (ht : RationalBits t B) (hT : RationalBits T B) (hp : RationalBits p B) :
    ∀ v ∈ mixingTrace a b m t T p, RationalBits v (12 * B + 6) := by
  have hab := rationalBits_add ha hb
  have habm := rationalBits_sub hab hm
  have hprod := rationalBits_mul ha hb
  have hU := rationalSecant_bits ha hb hm
  have hnum := rationalBits_sub ht hT
  have hden := rationalBits_sub hU hT
  have hr := rationalMixWeight_bits ha hb hm ht hT
  have hc := rationalBits_sub rationalBits_one hr
  have hbm := rationalBits_sub hb hm
  have hba := rationalBits_sub hb ha
  have hma := rationalBits_sub hm ha
  have hleft := rationalBits_div hbm hba
  have hright := rationalBits_div hma hba
  simp only [mixingTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono rationalBits_zero (by omega),
    rationalBits_mono rationalBits_one (by omega), rationalBits_mono ha (by omega),
    rationalBits_mono hb (by omega), rationalBits_mono hm (by omega),
    rationalBits_mono ht (by omega), rationalBits_mono hT (by omega),
    rationalBits_mono hp (by omega), rationalBits_mono hab (by omega),
    rationalBits_mono habm (by omega), rationalBits_mono hprod (by omega),
    rationalBits_mono hU (by omega), rationalBits_mono hnum (by omega),
    rationalBits_mono hden (by omega), rationalBits_mono hr (by omega),
    rationalBits_mono hc (by omega), rationalBits_mono hbm (by omega),
    rationalBits_mono hba (by omega), rationalBits_mono hma (by omega),
    rationalBits_mono hleft (by omega), rationalBits_mono hright (by omega),
    rationalBits_mono (rationalBits_mul hc hp) (by omega),
    rationalBits_mono (rationalBits_mul hr hleft) (by omega),
    rationalBits_mono (rationalBits_mul hr hright) (by omega)⟩

end ReciprocalAnchor.ManyLeaf
