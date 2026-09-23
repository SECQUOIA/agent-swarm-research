import Formal.MatroidSpectral.InterpolationBits
import Formal.MatroidSpectral.InterpolationTrace

/-! Polynomial bit charges for the actual materialized tensor interpolation run. -/
namespace MatroidSpectral
open ReciprocalAnchor DAGSpectral

lemma prodExpr_polynomial_bits {es : List ArithmeticExpr} {B : ℕ}
    (hv : ∀ a ∈ es, RationalBits a.eval B)
    (ht : ∀ a ∈ es, ∀ e ∈ a.trace, eventBits B e) :
    RationalBits (prodExpr es).eval (1+es.length*(B+1)) ∧
      ∀ e ∈ (prodExpr es).trace, eventBits (1+es.length*(B+1)) e := by
  induction es with
  | nil => simp [prodExpr, ArithmeticExpr.eval, ArithmeticExpr.trace, rationalBits_one]
  | cons a es ih =>
    obtain ⟨hval, htrace⟩ := ih (fun a ha => hv a (by simp [ha]))
      (fun a ha => ht a (by simp [ha]))
    have ha := hv a (by simp)
    have hsmall : B ≤ 1+(a::es).length*(B+1) := by
      simp only [List.length_cons]
      nlinarith
    have htail : 1+es.length*(B+1) ≤ 1+(a::es).length*(B+1) := by
      simp only [List.length_cons]
      nlinarith
    constructor
    · exact rationalBits_mono (rationalBits_mul ha hval) (by
        simp only [List.length_cons]
        nlinarith)
    · intro e he
      simp only [prodExpr, ArithmeticExpr.trace, List.mem_append, List.mem_singleton] at he
      rcases he with (he | he) | he
      · exact eventBits_mono (ht a (by simp) e he) hsmall
      · exact eventBits_mono (htrace e he) htail
      · subst e
        exact ⟨rationalBits_mono ha hsmall, rationalBits_mono hval htail⟩

lemma sumExpr_polynomial_bits {es : List ArithmeticExpr} {B : ℕ}
    (hv : ∀ a ∈ es, RationalBits a.eval B)
    (ht : ∀ a ∈ es, ∀ e ∈ a.trace, eventBits B e) :
    RationalBits (sumExpr es).eval (1+es.length*(B+1)) ∧
      ∀ e ∈ (sumExpr es).trace, eventBits (1+es.length*(B+1)) e := by
  induction es with
  | nil => simp [sumExpr, ArithmeticExpr.eval, ArithmeticExpr.trace, rationalBits_zero]
  | cons a es ih =>
    obtain ⟨hval, htrace⟩ := ih (fun a ha => hv a (by simp [ha]))
      (fun a ha => ht a (by simp [ha]))
    have ha := hv a (by simp)
    have hsmall : B ≤ 1+(a::es).length*(B+1) := by
      simp only [List.length_cons]
      nlinarith
    have htail : 1+es.length*(B+1) ≤ 1+(a::es).length*(B+1) := by
      simp only [List.length_cons]
      nlinarith
    constructor
    · exact rationalBits_mono (rationalBits_add ha hval) (by
        simp only [List.length_cons]
        nlinarith)
    · intro e he
      simp only [sumExpr, ArithmeticExpr.trace, List.mem_append, List.mem_singleton] at he
      rcases he with (he | he) | he
      · exact eventBits_mono (ht a (by simp) e he) hsmall
      · exact eventBits_mono (htrace e he) htail
      · subst e
        exact ⟨rationalBits_mono ha hsmall, rationalBits_mono hval htail⟩

lemma interpolationNumeratorTrace_bits (D N : ℕ) (xs : List ℚ)
    (hx : ∀ x ∈ xs, IntegralBound x N) :
    ∀ e ∈ (interpolationNumeratorTrace D xs).2,
      eventBits ((xs.length+1)*(N+2)) e := by
  induction xs with
  | nil => simp [interpolationNumeratorTrace]
  | cons x xs ih =>
    intro e he
    simp only [interpolationNumeratorTrace, List.mem_append] at he
    rcases he with he | he
    · exact eventBits_mono (ih (fun y hy => hx y (by simp [hy])) e he)
        (by
        simp only [List.length_cons]
        nlinarith)
    · obtain ⟨cell, hc, he⟩ := List.mem_flatMap.mp he
      obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hc
      simp only [interpolationNumeratorTrace_value] at he
      have hprev (j : ℕ) := interpolationNumeratorTable_integralBound D N xs
        (fun y hy => hx y (by simp [hy])) j
      have hx' := hx x (by simp)
      have ha : IntegralBound
          (if k.val = 0 then 0 else (interpolationNumeratorTable D xs).getD (k.val-1) 0)
          (xs.length*(N+1)) := by
        split_ifs
        · exact integralBound_zero _
        · exact hprev _
      have hp := hx'.mul (hprev k.val)
      simp only [List.mem_cons, List.not_mem_nil, or_false] at he
      rcases he with rfl | rfl
      · exact ⟨rationalBits_mono hx'.bits (by
        simp only [List.length_cons]
        nlinarith),
          rationalBits_mono (hprev k.val).bits (by
        simp only [List.length_cons]
        nlinarith)⟩
      · exact ⟨rationalBits_mono ha.bits (by
        simp only [List.length_cons]
        nlinarith),
          rationalBits_mono hp.bits (by
        simp only [List.length_cons]
        nlinarith)⟩

lemma interpolationDenominatorExpr_bits (D : ℕ) (t : Fin (D + 1)) :
    RationalBits (interpolationDenominatorExpr D t).eval (interpolationWeightBits D) ∧
    ∀ e ∈ (interpolationDenominatorExpr D t).trace, eventBits (interpolationWeightBits D) e := by
  have ht := (interpolationNode_integralBound t).bits
  have hv : ∀ a ∈ (interpolationOtherNodes D t).map (fun x =>
      ArithmeticExpr.op .sub (.atom (interpolationNode t)) (.atom x)),
      RationalBits a.eval (2*D+5) := by
    intro a ha
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp ha
    change RationalBits (interpolationNode t-x) _
    convert rationalBits_sub ht ((interpolationOtherNodes_integralBound D t x hx).bits) using 1
    ring
  have he : ∀ a ∈ (interpolationOtherNodes D t).map (fun x =>
      ArithmeticExpr.op .sub (.atom (interpolationNode t)) (.atom x)),
      ∀ e ∈ a.trace, eventBits (2*D+5) e := by
    intro a ha e he
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp ha
    simp only [ArithmeticExpr.trace, List.nil_append, List.mem_singleton] at he
    subst e
    exact ⟨rationalBits_mono ht (by omega),
      rationalBits_mono ((interpolationOtherNodes_integralBound D t x hx).bits) (by omega)⟩
  obtain ⟨hv', he'⟩ := prodExpr_polynomial_bits hv he
  have hb : 1+((interpolationOtherNodes D t).map (fun x =>
      ArithmeticExpr.op .sub (.atom (interpolationNode t)) (.atom x))).length*(2*D+5+1)
      ≤ interpolationWeightBits D := by
    simp only [List.length_map, interpolationOtherNodes_length, interpolationWeightBits]
    nlinarith
  exact ⟨rationalBits_mono hv' hb, fun e he => eventBits_mono (he' e he) hb⟩

lemma interpolationWeightTrace_bits (D : ℕ) (t : Fin (D + 1)) (k : ℕ) :
    ∀ e ∈ (interpolationWeightTrace D t k).2, eventBits (interpolationWeightBits D) e := by
  intro e he
  simp only [interpolationWeightTrace, ArithmeticExpr.run_eq, List.mem_append,
    List.mem_singleton] at he
  rcases he with (he | he) | he
  · apply eventBits_mono (interpolationNumeratorTrace_bits D (D+1) _
      (interpolationOtherNodes_integralBound D t) e he)
    rw [interpolationOtherNodes_length]
    unfold interpolationWeightBits
    nlinarith
  · exact (interpolationDenominatorExpr_bits D t).2 e he
  · subst e
    constructor
    · rw [interpolationNumeratorTrace_value]
      apply rationalBits_mono (interpolationNumeratorTable_bits D t k)
      unfold interpolationWeightBits
      nlinarith
    · exact (interpolationDenominatorExpr_bits D t).1

/-- A uniform budget for the tensor product and its value multiplication. -/
def interpolationTermBits (d D B : ℕ) : ℕ :=
  B+1+(d+1)*(interpolationWeightBits D+1)

section OrderedCoordinates
variable {κ : Type*} [Fintype κ] [LinearOrder κ]

lemma interpolationTermTrace_bits (D B : ℕ) (value : ℚ)
    (hv : RationalBits value B) (t z : κ → Fin (D + 1)) :
    RationalBits (interpolationTermTrace D value t z).1
        (interpolationTermBits (Fintype.card κ) D B) ∧
    ∀ e ∈ (interpolationTermTrace D value t z).2,
      eventBits (interpolationTermBits (Fintype.card κ) D B) e := by
  let ws := (interpolationCoordinateList κ).map
    (fun i => interpolationWeightTrace D (t i) (z i).val)
  have hw : ∀ w ∈ ws, RationalBits w.1 (interpolationWeightBits D) ∧
      ∀ e ∈ w.2, eventBits (interpolationWeightBits D) e := by
    intro w hw
    obtain ⟨i, _, rfl⟩ := List.mem_map.mp hw
    exact ⟨by rw [interpolationWeightTrace_value]; exact interpolationWeightRun_bits _ _ _,
      interpolationWeightTrace_bits _ _ _⟩
  have hp := prodExpr_polynomial_bits
    (es := ws.map (fun w => ArithmeticExpr.atom w.1))
    (B := interpolationWeightBits D)
    (by intro a ha; obtain ⟨w, hw', rfl⟩ := List.mem_map.mp ha; exact (hw w hw').1)
    (by intro a ha; obtain ⟨w, _, rfl⟩ := List.mem_map.mp ha; simp [ArithmeticExpr.trace])
  have hl : ws.length = Fintype.card κ := by simp [ws]
  have hprod : 1+(ws.map (fun w => ArithmeticExpr.atom w.1)).length*
      (interpolationWeightBits D+1) ≤ interpolationTermBits (Fintype.card κ) D B := by
    simp only [List.length_map, hl, interpolationTermBits]
    nlinarith
  have hweight : interpolationWeightBits D ≤ interpolationTermBits (Fintype.card κ) D B := by
    unfold interpolationTermBits
    nlinarith
  have hvalue : B ≤ interpolationTermBits (Fintype.card κ) D B := by
    unfold interpolationTermBits
    omega
  change RationalBits (value * (prodExpr (ws.map (fun w => .atom w.1))).run.1) _ ∧ _
  rw [ArithmeticExpr.run_eq]
  constructor
  · apply rationalBits_mono (rationalBits_mul hv hp.1)
    simp only [List.length_map, hl, interpolationTermBits]
    nlinarith
  · intro e he
    change e ∈ ws.flatMap Prod.snd ++
      (prodExpr (ws.map (fun w => .atom w.1))).run.2 ++
      [(.mul, value, (prodExpr (ws.map (fun w => .atom w.1))).run.1)] at he
    rw [ArithmeticExpr.run_eq] at he
    simp only [List.mem_append, List.mem_singleton] at he
    rcases he with (he | he) | he
    · obtain ⟨w, hw', he⟩ := List.mem_flatMap.mp he
      exact eventBits_mono ((hw w hw').2 e he) hweight
    · exact eventBits_mono (hp.2 e he) hprod
    · subst e
      exact ⟨rationalBits_mono hv hvalue, rationalBits_mono hp.1 hprod⟩

/-- Encoding budget for every arithmetic operand of the full tensor solve. -/
def interpolationTraceBits (d D B : ℕ) : ℕ :=
  1+(D+1)^d*(interpolationTermBits d D B+1)

lemma interpolateCoefficientTrace_bits (D B : ℕ)
    (values : (κ → Fin (D + 1)) → ℚ) (hv : ∀ t, RationalBits (values t) B)
    (z : κ → Fin (D + 1)) :
    ∀ e ∈ (interpolateCoefficientTrace D values z).2,
      eventBits (interpolationTraceBits (Fintype.card κ) D B) e := by
  let ts := (interpolationGridList κ D).map (fun t => interpolationTermTrace D (values t) t z)
  have ht : ∀ a ∈ ts, RationalBits a.1 (interpolationTermBits (Fintype.card κ) D B) ∧
      ∀ e ∈ a.2, eventBits (interpolationTermBits (Fintype.card κ) D B) e := by
    intro a ha
    obtain ⟨t, _, rfl⟩ := List.mem_map.mp ha
    exact interpolationTermTrace_bits D B _ (hv t) t z
  have hs := sumExpr_polynomial_bits
    (es := ts.map (fun a => ArithmeticExpr.atom a.1))
    (B := interpolationTermBits (Fintype.card κ) D B)
    (by intro a ha; obtain ⟨b, hb, rfl⟩ := List.mem_map.mp ha; exact (ht b hb).1)
    (by intro a ha; obtain ⟨b, _, rfl⟩ := List.mem_map.mp ha; simp [ArithmeticExpr.trace])
  have hlen : ts.length = (D+1)^(Fintype.card κ) := by
    simp [ts, interpolationGridList_length]
  have hone : 1 ≤ (D+1)^(Fintype.card κ) := Nat.one_le_pow _ _ (by omega)
  have hb : interpolationTermBits (Fintype.card κ) D B ≤
      interpolationTraceBits (Fintype.card κ) D B := by
    unfold interpolationTraceBits
    nlinarith
  intro e he
  change e ∈ ts.flatMap Prod.snd ++ (sumExpr (ts.map (fun a => .atom a.1))).run.2 at he
  rw [ArithmeticExpr.run_eq] at he
  rcases List.mem_append.mp he with he | he
  · obtain ⟨a, ha, he⟩ := List.mem_flatMap.mp he
    exact eventBits_mono ((ht a ha).2 e he) hb
  · simpa only [List.length_map, hlen, interpolationTraceBits] using hs.2 e he

/-- Schoolbook bit cost for the arithmetic actually executed by interpolation.
The separate evaluation of the input grid values belongs to the caller. -/
lemma interpolateCoefficientTrace_bitWork (D B : ℕ)
    (values : (κ → Fin (D + 1)) → ℚ) (hv : ∀ t, RationalBits (values t) B)
    (z : κ → Fin (D + 1)) :
    traceBitWork (interpolationTraceBits (Fintype.card κ) D B)
        (interpolateCoefficientTrace D values z).2 ≤
      (D+1)^(Fintype.card κ) *
        (Fintype.card κ*((2*(D+1)+2)*D+2)+2) *
        (256*(interpolationTraceBits (Fintype.card κ) D B+1)^3) := by
  simpa only [interpolateCoefficientTrace_length] using
    traceBitWork_le (interpolateCoefficientTrace_bits D B values hv z)

end OrderedCoordinates
end MatroidSpectral
