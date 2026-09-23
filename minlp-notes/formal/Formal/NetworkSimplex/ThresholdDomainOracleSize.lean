import Formal.NetworkSimplex.ThresholdDomainOracleCost
import Formal.NetworkSimplex.ThresholdDomainSize

/-! Bit bounds for every value in the actual domain-separator expression trees. -/
namespace NetworkSimplex.Chain.Threshold
open ReciprocalAnchor
namespace RationalData
variable {m L B : ℕ}

/-- Bound the output of every AST node; the b-flow constructor also records
both arithmetic intermediates hidden by the coordinate accessor. -/
def DomainEvalBits (D : RationalData m L) (W : ℕ)
    (e : AffineExpression (Coordinate m (Fin L))) : Prop :=
  RationalBits (e.evalRat D.coordinatesRat) W ∧ match e with
  | .constant _ => True
  | .variable (.bFlow i) => RationalBits (1 - D.xh) W ∧ RationalBits (D.oppositeFlow i) W
  | .variable _ => True
  | .add a b => DomainEvalBits D W a ∧ DomainEvalBits D W b
  | .neg a => DomainEvalBits D W a

def domainOperandBits (m B : ℕ) := 2 * B + 8 + (m + 1) * (B + 1)

private theorem bits_mono {q : ℚ} {a b : ℕ} (h : RationalBits q a) (hab : a ≤ b) :
    RationalBits q b := rationalBits_mono h hab

/-- Includes inactive zero-product placeholders, negated flow coordinates,
and both opposite-flow subtraction intermediates. -/
theorem domainExpressionRat_all_bits {D : RationalData m L} (h : D.InputBits B)
    (r : DomainRow m (Fin L)) :
    DomainEvalBits D (domainOperandBits m B) (D.domainExpressionRat r) := by
  have hi {q : ℚ} (hq : RationalBits q B) := bits_mono hq
    (show B ≤ domainOperandBits m B by unfold domainOperandBits; omega)
  have hz := bits_mono rationalBits_zero
    (show 1 ≤ domainOperandBits m B by unfold domainOperandBits; omega)
  have ho := bits_mono rationalBits_one
    (show 1 ≤ domainOperandBits m B by unfold domainOperandBits; omega)
  have hh := bits_mono (domain_bypass_complement_bits h)
    (show B + 2 ≤ domainOperandBits m B by unfold domainOperandBits; omega)
  have ha (i : Fin L) := bits_mono (domain_arc_complement_bits h i)
    (show B + 2 ≤ domainOperandBits m B by unfold domainOperandBits; omega)
  have hb (i : Fin L) := bits_mono (oppositeFlow_bits h i)
    (show 2 * B + 3 ≤ domainOperandBits m B by unfold domainOperandBits; omega)
  have hbc (i : Fin L) := bits_mono (oppositeFlow_complement_bits h i)
    (show 2 * B + 5 ≤ domainOperandBits m B by unfold domainOperandBits; omega)
  cases r <;> simp only [domainExpressionRat] <;> (try split_ifs) <;>
    simp only [DomainEvalBits, AffineExpression.evalRat, coordinatesRat, and_true]
  all_goals first
    | exact hi h.xh
    | exact ⟨by simpa [sub_eq_add_neg] using hh, ho, rationalBits_neg (hi h.xh), hi h.xh⟩
    | exact hi (h.xa _)
    | exact ⟨by simpa [sub_eq_add_neg] using ha _, ho,
        rationalBits_neg (hi (h.xa _)), hi (h.xa _)⟩
    | exact ⟨hb _, hh, hb _⟩
    | exact ⟨by simpa [sub_eq_add_neg] using hbc _, ho,
        rationalBits_neg (hb _), hb _, hh, hb _⟩
    | exact hi (h.weights _)
    | exact hi (h.u _ _)
    | exact hi (h.v _ _)
    | exact hi (h.zh _)
    | exact hz

private theorem evalRat_sumList (D : RationalData m L)
    (es : List (AffineExpression (Coordinate m (Fin L)))) :
    (AffineExpression.sumList es).evalRat D.coordinatesRat =
      (es.map (AffineExpression.evalRat D.coordinatesRat)).sum := by
  induction es with
  | nil => rfl
  | cons e es ih => simp [AffineExpression.sumList, AffineExpression.evalRat, ih]

/-- All recursive suffix accumulators of the weight sum are covered, independently
of whether the weights are nonnegative or normalized. -/
theorem weightAst_all_bits {D : RationalData m L} (h : D.InputBits B)
    (js : List (Fin (m + 1))) (hlen : js.length ≤ m + 1) :
    DomainEvalBits D (domainOperandBits m B)
      (AffineExpression.sumList (js.map fun j => .variable (.weight j))) := by
  induction js with
  | nil =>
    exact ⟨bits_mono rationalBits_zero (by unfold domainOperandBits; omega), trivial⟩
  | cons j js ih =>
    have hsum : RationalBits ((js.map D.weights).sum) (1 + (m + 1) * (B + 1)) := by
      apply input_sum_bits h
      · intro q hq; obtain ⟨k, _, rfl⟩ := List.mem_map.mp hq; exact h.weights k
      · simp only [List.length_map]; simp only [List.length_cons] at hlen; omega
    have hfull : RationalBits (D.weights j + (js.map D.weights).sum)
        (1 + (m + 1) * (B + 1)) := by
      apply input_sum_bits h (xs := (j :: js).map D.weights)
      · intro q hq; obtain ⟨k, _, rfl⟩ := List.mem_map.mp hq; exact h.weights k
      · simpa only [List.length_map] using hlen
    refine ⟨?_, ?_, ih (by simp only [List.length_cons] at hlen; omega)⟩
    · simpa [List.map_cons, AffineExpression.sumList, AffineExpression.evalRat,
        coordinatesRat, evalRat_sumList, List.map_map, Function.comp_def] using
        bits_mono hfull (show 1 + (m + 1) * (B + 1) ≤ domainOperandBits m B by
          unfold domainOperandBits; omega)
    · exact ⟨bits_mono (h.weights j) (by unfold domainOperandBits; omega), trivial⟩

/-- Both sides of simplex equality and every recursive AST intermediate have
polynomial bit length under the raw input-size assumption. -/
theorem domainCutExpression_all_bits {D : RationalData m L} (h : D.InputBits B)
    (tag : DomainCutIndex m L) :
    DomainEvalBits D (domainOperandBits m B) (D.domainCutExpression tag) := by
  have hw := weightAst_all_bits h (List.ofFn (fun j : Fin (m + 1) => j)) (by simp)
  have hw' : DomainEvalBits D (domainOperandBits m B)
      (AffineExpression.sum fun j => .variable (.weight j)) := by
    simpa [AffineExpression.sum, List.map_ofFn, Function.comp_def] using hw
  have hsum : RationalBits (List.ofFn D.weights).sum (1 + (m + 1) * (B + 1)) := by
    simpa only [(weightSum_spec _).1] using weightSum_partial_bits h (List.Sublist.refl _)
  have hs : RationalBits (simplexExpression.evalRat D.coordinatesRat)
      (domainOperandBits m B) := by
    have hh := rationalBits_add hsum (rationalBits_neg rationalBits_one)
    apply bits_mono _ (show 1 + (m + 1) * (B + 1) + 1 + 1 ≤ domainOperandBits m B by
      unfold domainOperandBits; omega)
    simpa [simplexExpression, AffineExpression.evalRat, AffineExpression.sum,
      evalRat_sumList, List.map_ofFn, coordinatesRat, Function.comp_def] using hh
  have hs' : DomainEvalBits D (domainOperandBits m B) simplexExpression :=
    ⟨hs, hw', bits_mono (rationalBits_neg rationalBits_one)
      (by unfold domainOperandBits; omega), trivial⟩
  rcases tag with r | b
  · exact domainExpressionRat_all_bits h r
  · cases b
    · exact ⟨rationalBits_neg hs, hs'⟩
    · exact hs'

/-- In particular, all values passed to the negative-cut scan satisfy the bound. -/
theorem domainCutValues_bits {D : RationalData m L} (h : D.InputBits B)
    (z : DomainCutIndex m L × (ℚ × ℕ)) (hz : z ∈ D.domainCutValues) :
    RationalBits z.2.1 (domainOperandBits m B) := by
  obtain ⟨tag, _, rfl⟩ := List.mem_map.mp hz
  rw [(domainEvalRun_spec D _).1]
  have hh := domainCutExpression_all_bits h tag
  unfold DomainEvalBits at hh
  exact hh.1

end RationalData
end NetworkSimplex.Chain.Threshold
