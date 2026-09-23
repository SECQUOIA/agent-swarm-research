import Formal.NetworkSimplex.ThresholdDomainExpressions

/-! Executable domain separation with literal affine output and global validity. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
namespace RationalData
variable {m L : ℕ}

/-- Scan all cached values, retaining an actual negative entry if one exists. -/
def negativeCutRun {α : Type*} : List (α × ℚ) → Option α × ℕ
  | [] => (none, 0)
  | (tag, q) :: rest =>
      let tail := negativeCutRun rest
      (if q < 0 then some tag else tail.1, 1 + tail.2)

theorem negativeCutRun_none {α : Type*} (qs : List (α × ℚ)) :
    (negativeCutRun qs).1 = none ↔ ∀ z ∈ qs, 0 ≤ z.2 := by
  induction qs with
  | nil => simp [negativeCutRun]
  | cons z qs ih =>
    rcases z with ⟨tag, q⟩
    by_cases hq : q < 0
    · simp [negativeCutRun, hq, not_le.mpr hq]
    · simp [negativeCutRun, hq, ih, le_of_not_gt hq]

theorem negativeCutRun_some {α : Type*} (qs : List (α × ℚ)) {tag : α}
    (h : (negativeCutRun qs).1 = some tag) : ∃ q, (tag, q) ∈ qs ∧ q < 0 := by
  induction qs with
  | nil => simp [negativeCutRun] at h
  | cons z qs ih =>
    rcases z with ⟨key, q⟩
    by_cases hq : q < 0
    · have ht : key = tag := by simpa [negativeCutRun, hq] using h
      subst key
      exact ⟨q, by simp, hq⟩
    · obtain ⟨q', hmem, hneg⟩ := ih (by simpa [negativeCutRun, hq] using h)
      exact ⟨q', List.mem_cons_of_mem _ hmem, hneg⟩

theorem negativeCutRun_charge {α : Type*} (qs : List (α × ℚ)) :
    (negativeCutRun qs).2 = qs.length := by
  induction qs with
  | nil => rfl
  | cons z qs ih => cases z; simp [negativeCutRun, ih, Nat.add_comm]

/-- Arithmetic performed by direct AST evaluation; b-flow access reconstructs
`1 - xh - xa` using two subtractions. Other coordinate accesses are inputs. -/
def domainEvalOps : AffineExpression (Coordinate m (Fin L)) → ℕ
  | .constant _ => 0
  | .variable (.bFlow _) => 2
  | .variable _ => 0
  | .add e f => domainEvalOps e + domainEvalOps f + 1
  | .neg e => domainEvalOps e + 1

/-- Literal arithmetic evaluator, with an exact operation counter. -/
def domainEvalRun (D : RationalData m L) :
    AffineExpression (Coordinate m (Fin L)) → ℚ × ℕ
  | .constant q => (q, 0)
  | .variable z => (D.coordinatesRat z, match z with | .bFlow _ => 2 | _ => 0)
  | .add e f =>
      let a := domainEvalRun D e
      let b := domainEvalRun D f
      (a.1 + b.1, a.2 + b.2 + 1)
  | .neg e => let a := domainEvalRun D e; (-a.1, a.2 + 1)

theorem domainEvalRun_spec (D : RationalData m L)
    (e : AffineExpression (Coordinate m (Fin L))) :
    (D.domainEvalRun e).1 = e.evalRat D.coordinatesRat ∧
      (D.domainEvalRun e).2 = domainEvalOps e := by
  induction e with
  | constant q => exact ⟨rfl, rfl⟩
  | «variable» z => cases z <;> exact ⟨rfl, rfl⟩
  | add e f he hf => simp [domainEvalRun, AffineExpression.evalRat, domainEvalOps, he, hf]
  | neg e he => simp [domainEvalRun, AffineExpression.evalRat, domainEvalOps, he]

/-- Each candidate is either a domain margin or one side of simplex equality. -/
abbrev DomainCutIndex (m L : ℕ) := DomainRow m (Fin L) ⊕ Bool

def domainCutExpression (D : RationalData m L) : DomainCutIndex m L →
    AffineExpression (Coordinate m (Fin L))
  | .inl r => D.domainExpressionRat r
  | .inr b => if b then simplexExpression else .neg simplexExpression

def domainCutTags (m L : ℕ) : List (DomainCutIndex m L) :=
  (domainTags m L).map Sum.inl ++ [Sum.inr true, Sum.inr false]

/-- Values and evaluation charges are generated once per candidate. -/
def domainCutValues (D : RationalData m L) :
    List (DomainCutIndex m L × (ℚ × ℕ)) :=
  (domainCutTags m L).map fun tag => (tag, D.domainEvalRun (D.domainCutExpression tag))

def domainOracle (D : RationalData m L) : Option (DomainCutIndex m L) × ℕ :=
  let values := D.domainCutValues
  let scan := negativeCutRun (values.map fun z => (z.1, z.2.1))
  (scan.1, scan.2 + (values.map fun z => z.2.2).sum)

theorem mem_domainCutTags (tag : DomainCutIndex m L) : tag ∈ domainCutTags m L := by
  rcases tag with r | b
  · exact List.mem_append_left _ (List.mem_map.mpr ⟨r, mem_domainTags r, rfl⟩)
  · cases b <;> simp [domainCutTags]

theorem evalRat_coordinates_cast (D : RationalData m L)
    (e : AffineExpression (Coordinate m (Fin L))) :
    (e.evalRat D.coordinatesRat : ℝ) = e.eval (coordinates D.toReal D.toReal.xb) := by
  rw [AffineExpression.evalRat_cast]
  congr 1
  funext z
  exact D.coordinatesRat_cast z

theorem domainOracle_none_values (D : RationalData m L) :
    D.domainOracle.1 = none ↔ ∀ tag, 0 ≤ (D.domainCutExpression tag).evalRat D.coordinatesRat := by
  simp only [domainOracle, negativeCutRun_none, domainCutValues, List.forall_mem_map]
  constructor
  · intro h tag
    simpa only [(domainEvalRun_spec D _).1] using h tag (mem_domainCutTags tag)
  · intro h tag _
    simpa only [(domainEvalRun_spec D _).1] using h tag

/-- Accepting the domain oracle is exactly membership in the original domain.
The residual label has no observed products, as in the reduced chain model. -/
theorem domainOracle_none_iff (D : RationalData m L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.domainOracle.1 = none ↔ D.toReal.OriginalDomain := by
  rw [domainOracle_none_values, originalDomain_iff_domainExpressions D.toReal hc hh]
  constructor
  · intro h
    have hp := h (Sum.inr true)
    have hn := h (Sum.inr false)
    change 0 ≤ simplexExpression.evalRat D.coordinatesRat at hp
    change 0 ≤ -simplexExpression.evalRat D.coordinatesRat at hn
    have heq : (simplexExpression : AffineExpression (Coordinate m (Fin L))).evalRat
        D.coordinatesRat = 0 := by linarith
    refine ⟨fun r => ?_, ?_⟩
    · have hr := h (Sum.inl r)
      change 0 ≤ (D.domainExpressionRat r).evalRat D.coordinatesRat at hr
      have hr' : (0 : ℝ) ≤ ((D.domainExpressionRat r).evalRat D.coordinatesRat : ℝ) := by
        exact_mod_cast hr
      simpa only [evalRat_coordinates_cast, domainExpressionRat_eq] using hr'
    · rw [← evalRat_coordinates_cast, heq, Rat.cast_zero]
  · rintro ⟨hr, hs⟩ tag
    rcases tag with r | b
    · change 0 ≤ (D.domainExpressionRat r).evalRat D.coordinatesRat
      have hreal : (0 : ℝ) ≤ ((D.domainExpressionRat r).evalRat D.coordinatesRat : ℝ) := by
        simpa only [evalRat_coordinates_cast, domainExpressionRat_eq] using hr r
      exact_mod_cast hreal
    · have hrat : (simplexExpression : AffineExpression (Coordinate m (Fin L))).evalRat
          D.coordinatesRat = 0 := by
        rw [← evalRat_coordinates_cast] at hs
        exact_mod_cast hs
      cases b <;> simp [domainCutExpression, AffineExpression.evalRat, hrat]

/-- Every returned tag identifies an affine inequality strictly violated by the
actual rational query. -/
theorem domainOracle_some_negative (D : RationalData m L) {tag : DomainCutIndex m L}
    (h : D.domainOracle.1 = some tag) :
    (D.domainCutExpression tag).evalRat D.coordinatesRat < 0 := by
  obtain ⟨q, hmem, hq⟩ := negativeCutRun_some _ h
  simp only [domainCutValues, List.map_map, List.mem_map] at hmem
  obtain ⟨key, _, he⟩ := hmem
  have hk : key = tag := congrArg Prod.fst he
  subst key
  have hv : (D.domainEvalRun (D.domainCutExpression tag)).1 = q := congrArg Prod.snd he
  rw [(D.domainEvalRun_spec _).1] at hv
  exact hv ▸ hq

/-- Each candidate is globally valid at every real original-domain point with
this same observation pattern, not just at the current rational input. -/
theorem domainCutExpression_valid (D : RationalData m L) (tag : DomainCutIndex m L)
    (E : ReductionData m (Fin L)) (hp : D.c = E.c) (ho : D.observedH = E.observedH)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (hE : E.OriginalDomain) :
    0 ≤ (D.domainCutExpression tag).eval (coordinates E E.xb) := by
  have hec : ∀ i, E.c i 0 = .neither := by rw [← hp]; exact hc
  have heh : E.observedH 0 = false := by rw [← ho]; exact hh
  have hs := (originalDomain_iff_fixed_domainExpressions D.toReal E hp ho hec heh).mp hE
  rcases tag with r | b
  · change 0 ≤ (D.domainExpressionRat r).eval (coordinates E E.xb)
    rw [domainExpressionRat_eq]
    exact hs.1 r
  · cases b <;> simp [domainCutExpression, AffineExpression.eval, hs.2]

/-- The executable public output includes the literal affine syntax tree. -/
def domainSeparator (D : RationalData m L) :
    Option (AffineExpression (Coordinate m (Fin L))) × ℕ :=
  let result := D.domainOracle
  (result.1.map D.domainCutExpression, result.2)

theorem domainSeparator_none_iff (D : RationalData m L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.domainSeparator.1 = none ↔ D.toReal.OriginalDomain := by
  simpa only [domainSeparator, Option.map_eq_none_iff] using D.domainOracle_none_iff hc hh

/-- A returned affine cut is violated and valid on the entire real domain. -/
theorem domainSeparator_some (D : RationalData m L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    {e : AffineExpression (Coordinate m (Fin L))} (h : D.domainSeparator.1 = some e) :
    e.evalRat D.coordinatesRat < 0 ∧
      ∀ E : ReductionData m (Fin L), D.c = E.c → D.observedH = E.observedH →
        E.OriginalDomain → 0 ≤ e.eval (coordinates E E.xb) := by
  obtain ⟨tag, htag, rfl⟩ := Option.map_eq_some_iff.mp h
  exact ⟨D.domainOracle_some_negative htag,
    fun E hp ho hE => D.domainCutExpression_valid tag E hp ho hc hh hE⟩

/-- Every domain cut has unit coefficients even on the state weights. -/
theorem domainCutExpression_unit (D : RationalData m L) (tag : DomainCutIndex m L)
    (z : Coordinate m (Fin L)) :
    -1 ≤ (D.domainCutExpression tag).coefficient z ∧
      (D.domainCutExpression tag).coefficient z ≤ 1 := by
  rcases tag with r | b
  · change -1 ≤ (D.domainExpressionRat r).coefficient z ∧
      (D.domainExpressionRat r).coefficient z ≤ 1
    rw [domainExpressionRat_eq]
    exact domainExpression_coefficient D.toReal r z
  · cases b
    · change -1 ≤ -simplexExpression.coefficient z ∧ -simplexExpression.coefficient z ≤ 1
      have h := simplexExpression_coefficient_unit z
      omega
    · exact simplexExpression_coefficient_unit z

theorem domainSeparator_some_unit (D : RationalData m L)
    {e : AffineExpression (Coordinate m (Fin L))} (h : D.domainSeparator.1 = some e)
    (z : Coordinate m (Fin L)) : -1 ≤ e.coefficient z ∧ e.coefficient z ≤ 1 := by
  obtain ⟨tag, _, rfl⟩ := Option.map_eq_some_iff.mp h
  exact D.domainCutExpression_unit tag z

end RationalData
end NetworkSimplex.Chain.Threshold
