import Formal.NetworkSimplex.ThresholdRows
import Formal.NetworkSimplex.ProfileHull

/-! Literal affine rows for the original chain domain checks. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

/-- A finite original-domain row index, including each actual flow box. -/
inductive DomainRow (m : ℕ) (I : Type*) where
  | bypassLower | bypassUpper
  | aLower : I → DomainRow m I
  | aUpper : I → DomainRow m I
  | bLower : I → DomainRow m I
  | bUpper : I → DomainRow m I
  | weightLower : Fin (m + 1) → DomainRow m I
  | aProductLower : I → Fin m → DomainRow m I
  | bProductLower : I → Fin m → DomainRow m I
  | bypassProductLower : Fin m → DomainRow m I
  deriving DecidableEq, Fintype

variable {m : ℕ} {I : Type*}

/-- Unobserved products give the tautology zero; every other margin is a literal domain row. -/
def domainExpression (D : ReductionData m I) : DomainRow m I → AffineExpression (Coordinate m I)
  | .bypassLower => .variable .bypassFlow
  | .bypassUpper => .add (.constant 1) (.neg (.variable .bypassFlow))
  | .aLower i => .variable (.aFlow i)
  | .aUpper i => .add (.constant 1) (.neg (.variable (.aFlow i)))
  | .bLower i => .variable (.bFlow i)
  | .bUpper i => .add (.constant 1) (.neg (.variable (.bFlow i)))
  | .weightLower j => .variable (.weight j)
  | .aProductLower i j => if observesA (D.c i j.succ) then
      .variable (.aProduct i j) else .constant 0
  | .bProductLower i j => if observesB (D.c i j.succ) then
      .variable (.bProduct i j) else .constant 0
  | .bypassProductLower j => if D.observedH j.succ then
      .variable (.bypassProduct j) else .constant 0

/-- The simplex normalization equation, written as an affine expression equal to zero. -/
def simplexExpression : AffineExpression (Coordinate m I) :=
  .add (AffineExpression.sum fun j : Fin (m + 1) => .variable (.weight j)) (.constant (-1))

theorem simplexExpression_eval (D : ReductionData m I) (xb : I → ℝ) :
    simplexExpression.eval (coordinates D xb) = (∑ j, D.weights j) - 1 := by
  simp [simplexExpression, AffineExpression.eval, coordinates, sub_eq_add_neg]

/-- Every domain margin has signed unit coefficients, including the weight coordinates. -/
theorem domainExpression_coefficient [DecidableEq I] (D : ReductionData m I)
    (r : DomainRow m I) (c : Coordinate m I) :
    -1 ≤ (domainExpression D r).coefficient c ∧ (domainExpression D r).coefficient c ≤ 1 := by
  cases r <;> simp only [domainExpression] <;> (try split_ifs) <;>
    simp only [AffineExpression.coefficient] <;> (try split_ifs) <;> norm_num

theorem simplexExpression_coefficient [DecidableEq I] (c : Coordinate m I) :
    simplexExpression.coefficient c = match c with | .weight _ => 1 | _ => 0 := by
  cases c <;> simp [simplexExpression, AffineExpression.coefficient]

theorem simplexExpression_coefficient_unit [DecidableEq I] (c : Coordinate m I) :
    -1 ≤ simplexExpression.coefficient c ∧ simplexExpression.coefficient c ≤ 1 := by
  rw [simplexExpression_coefficient]
  cases c <;> norm_num

/-- Domain rows are fixed by the observation pattern, not the queried values. -/
theorem domainExpression_eq_of_pattern_eq (D E : ReductionData m I)
    (hc : D.c = E.c) (hh : D.observedH = E.observedH) (r : DomainRow m I) :
    domainExpression D r = domainExpression E r := by
  cases r <;> simp [domainExpression, hc, hh]

/-- Evaluating all domain margins gives precisely the boxes, simplex nonnegativity,
and observed-product nonnegativity on the explicit labels. -/
theorem domainExpressions_iff (D : ReductionData m I) (xb : I → ℝ) :
    (∀ r, 0 ≤ (domainExpression D r).eval (coordinates D xb)) ↔
      (0 ≤ D.xh ∧ D.xh ≤ 1) ∧
      (∀ i, 0 ≤ D.xa i ∧ D.xa i ≤ 1) ∧
      (∀ i, 0 ≤ xb i ∧ xb i ≤ 1) ∧
      (∀ j, 0 ≤ D.weights j) ∧
      (∀ i (j : Fin m), observesA (D.c i j.succ) → 0 ≤ D.u i j.succ) ∧
      (∀ i (j : Fin m), observesB (D.c i j.succ) → 0 ≤ D.v i j.succ) ∧
      (∀ j : Fin m, D.observedH j.succ = true → 0 ≤ D.zh j.succ) := by
  constructor
  · intro h
    have hb := h .bypassLower
    have ht := h .bypassUpper
    simp only [domainExpression, AffineExpression.eval, coordinates, Rat.cast_one] at hb ht
    refine ⟨⟨hb, by linarith⟩, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · intro i
      have hl := h (.aLower i)
      have hu := h (.aUpper i)
      simp only [domainExpression, AffineExpression.eval, coordinates, Rat.cast_one] at hl hu
      exact ⟨hl, by linarith⟩
    · intro i
      have hl := h (.bLower i)
      have hu := h (.bUpper i)
      simp only [domainExpression, AffineExpression.eval, coordinates, Rat.cast_one] at hl hu
      exact ⟨hl, by linarith⟩
    · exact fun j => h (.weightLower j)
    · intro i j hj
      simpa [domainExpression, hj, AffineExpression.eval, coordinates] using h (.aProductLower i j)
    · intro i j hj
      simpa [domainExpression, hj, AffineExpression.eval, coordinates] using h (.bProductLower i j)
    · intro j hj
      simpa [domainExpression, hj, AffineExpression.eval, coordinates] using
        h (.bypassProductLower j)
  · rintro ⟨hh, ha, hb, hw, hpa, hpb, hph⟩ r
    cases r with
    | bypassLower => exact hh.1
    | bypassUpper =>
      simpa [domainExpression, AffineExpression.eval, coordinates] using sub_nonneg.mpr hh.2
    | aLower i => exact (ha i).1
    | aUpper i =>
      simpa [domainExpression, AffineExpression.eval, coordinates] using sub_nonneg.mpr (ha i).2
    | bLower i => exact (hb i).1
    | bUpper i =>
      simpa [domainExpression, AffineExpression.eval, coordinates] using sub_nonneg.mpr (hb i).2
    | weightLower j => exact hw j
    | aProductLower i j =>
      by_cases h : observesA (D.c i j.succ) <;>
        simp [domainExpression, h, AffineExpression.eval, coordinates, hpa i j]
    | bProductLower i j =>
      by_cases h : observesB (D.c i j.succ) <;>
        simp [domainExpression, h, AffineExpression.eval, coordinates, hpb i j]
    | bypassProductLower j =>
      cases h : D.observedH j.succ <;>
        simp [domainExpression, h, AffineExpression.eval, coordinates, hph j]

/-- The original-domain prechecks are a finite affine description with actual b-flow
coordinates. Only the unobserved residual products are omitted. -/
theorem originalDomain_iff_domainExpressions {L : ℕ} (D : ReductionData m (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.OriginalDomain ↔
      (∀ r, 0 ≤ (domainExpression D r).eval (coordinates D D.xb)) ∧
      simplexExpression.eval (coordinates D D.xb) = 0 := by
  rw [domainExpressions_iff, simplexExpression_eval]
  constructor
  · rintro ⟨⟨hw, hsum⟩, hf, hp, hph⟩
    have hf' := ((flow_iff L _ 1).mp hf).1
    refine ⟨⟨?_, ?_, ?_, hw, ?_, ?_, ?_⟩, by linarith⟩
    · exact hf' bypass
    · exact fun i => hf' (a i)
    · exact fun i => hf' (b i)
    · exact fun i j => (hp i).1 j.succ
    · exact fun i j => (hp i).2 j.succ
    · exact fun j => hph j.succ
  · rintro ⟨⟨hxh, hxa, hxb, hw, hpa, hpb, hph⟩, hsum⟩
    refine ⟨⟨hw, by linarith⟩, ?_, ?_, ?_⟩
    · apply (flow_iff L _ 1).mpr
      constructor
      · intro e
        rcases e with ⟨i, flag⟩ | u
        · cases flag
          · exact hxa i
          · exact hxb i
        · exact hxh
      · intro i
        simp only [pack_a, pack_b, pack_bypass, ReductionData.xb]
        ring
    · intro i
      constructor
      · intro j
        refine Fin.cases ?_ (fun k => hpa i k) j
        simp [hc i, observesA]
      · intro j
        refine Fin.cases ?_ (fun k => hpb i k) j
        simp [hc i, observesB]
    · intro j
      refine Fin.cases ?_ (fun k => hph k) j
      simp [hh]

/-- A fixed instance's affine domain description is exact at every query with the same
observation pattern. -/
theorem originalDomain_iff_fixed_domainExpressions {L : ℕ}
    (D E : ReductionData m (Fin L)) (hpattern : D.c = E.c)
    (hobserved : D.observedH = E.observedH)
    (hc : ∀ i, E.c i 0 = .neither) (hh : E.observedH 0 = false) :
    E.OriginalDomain ↔
      (∀ r, 0 ≤ (domainExpression D r).eval (coordinates E E.xb)) ∧
      simplexExpression.eval (coordinates E E.xb) = 0 := by
  simp only [domainExpression_eq_of_pattern_eq D E hpattern hobserved]
  exact originalDomain_iff_domainExpressions E hc hh

end NetworkSimplex.Chain.Threshold
