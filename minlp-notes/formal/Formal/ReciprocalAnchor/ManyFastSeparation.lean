import Formal.ReciprocalAnchor.ManyFastSize
import Formal.ReciprocalAnchor.ManySeparation

/-! Executable extraction of a rational separating cut from the fast envelope output. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope
open MeasureTheory Set

/-- A literal linear search, avoiding any noncomputable choice of a source line. -/
def lookupSource {N : ℕ} (source : Fin N → Line) (target : Line) :
    List (Fin N) → Option (Fin N) × ℕ
  | [] => (none, 0)
  | i :: rest => if source i = target then (some i, 1)
      else let r := lookupSource source target rest; (r.1, r.2 + 1)

theorem lookupSource_correct {N : ℕ} (source : Fin N → Line) (target : Line)
    (indices : List (Fin N)) (h : ∃ i ∈ indices, source i = target) :
    ∃ i, (lookupSource source target indices).1 = some i ∧ source i = target := by
  induction indices with
  | nil => simp at h
  | cons i rest ih =>
    by_cases hi : source i = target
    · exact ⟨i, by simp [lookupSource, hi], hi⟩
    · obtain ⟨j, hj, heq⟩ := h
      have hj' : j ∈ rest := by
        rcases List.mem_cons.mp hj with rfl | hj
        · exact False.elim (hi heq)
        · exact hj
      obtain ⟨k, hk, he⟩ := ih ⟨j, hj', heq⟩
      exact ⟨k, by simpa only [lookupSource, hi, ↓reduceIte] using hk, he⟩

theorem lookupSource_cost {N : ℕ} (source : Fin N → Line) (target : Line)
    (indices : List (Fin N)) : (lookupSource source target indices).2 ≤ indices.length := by
  induction indices with
  | nil => simp [lookupSource]
  | cons i rest ih =>
    by_cases hi : source i = target <;> simp only [lookupSource, hi, ↓reduceIte, List.length_cons]
    · omega
    · omega

/-- The input family with its original index retained. -/
def sourceLine {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) (i : Fin (2 * n + 2)) : Line :=
  ⟨-(rationalLines m q w i).negSlope, (rationalLines m q w i).intercept⟩

def sourceIndex {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) (l : Line) : Fin (2 * n + 2) :=
  (lookupSource (sourceLine m q w) l (List.finRange (2 * n + 2))).1.getD 0

theorem sourceIndex_correct {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) {l : Line}
    (hl : l ∈ sourceLines m q w) : sourceLine m q w (sourceIndex m q w l) = l := by
  obtain ⟨i, hi⟩ := List.mem_ofFn.mp hl
  have hex : ∃ i ∈ List.finRange (2 * n + 2), sourceLine m q w i = l :=
    ⟨i, List.mem_finRange i, hi⟩
  obtain ⟨j, hj, he⟩ := lookupSource_correct (sourceLine m q w) l _ hex
  simpa only [sourceIndex, hj, Option.getD_some] using he

/-- Produce rational coefficients from the actual sorted-stack segments. -/
def fastCut {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) : RationalAffineForm n :=
  (1 / a + a / a ^ 2, -(1 / a ^ 2), 0, 0) +
    (((buildSegments (sourceLines m q w) a b).1).map fun s =>
      segmentForm (sourceIndex m q w s.active) s.lo s.hi).sum

theorem RationalAffineForm_eval_list_sum {n : ℕ} (forms : List (RationalAffineForm n))
    (m : ℝ) (q w : Fin n → ℝ) : forms.sum.eval m q w =
      (forms.map fun F => F.eval m q w).sum := by
  induction forms with
  | nil => simp
  | cons F rest ih => simp only [List.sum_cons, RationalAffineForm.eval_add,
      List.map_cons, ih]

/-- Every segment's recovered source index gives the same line at the candidate. -/
theorem built_segment_source_eval {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    {s : Segment} (hs : s ∈ (buildSegments (sourceLines m q w) a b).1) (x : ℝ) :
    line (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ))
      (sourceIndex m q w s.active) x = s.active.evalReal x := by
  have hm := buildStack_members _ (segments_active_mem _ _ _ hs)
  rw [← sourceLine_eval]
  exact congrArg (fun l : Line => l.evalReal x) (sourceIndex_correct m q w hm)

/-- The extracted affine coefficients evaluate to the exact fast lower moment. -/
theorem fastCut_exact {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a ≤ b) :
    (fastCut a b m q w).eval m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) =
      (fastLowerMoment a b m q w : ℝ) := by
  let ss := (buildSegments (sourceLines m q w) a b).1
  have he (s : Segment) (hs : s ∈ ss) :
      (segmentForm (sourceIndex m q w s.active) s.lo s.hi).eval m
        (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) = (s.integral : ℝ) := by
    have hb := segments_bounds (buildStack (sourceLines m q w)).1 a b hab hs
    rw [segmentForm_eval_eq_integral _ (ha.trans_le hb.1) hb.2.1,
      s.integral_eq (ha.trans_le hb.1) hb.2.1]
    apply intervalIntegral.integral_congr
    intro x _
    simp only [built_segment_source_eval hs]
  unfold fastCut fastLowerMoment
  rw [RationalAffineForm.eval_add, RationalAffineForm_eval_list_sum, List.map_map]
  push_cast
  have hsum : (ss.map fun s => (segmentForm (sourceIndex m q w s.active) s.lo s.hi).eval m
      (fun j => (q j : ℝ)) (fun j => (w j : ℝ))).sum =
      (ss.map fun s => (s.integral : ℝ)).sum := by
    congr 1
    exact List.map_congr_left he
  rw [List.map_map]
  change _ + (ss.map _).sum = _ + (ss.map fun s => (s.integral : ℝ)).sum
  simp only [Function.comp_def]
  rw [hsum]
  congr 1
  simp [RationalAffineForm.eval]
  ring

/-- The output coefficients remain valid at every other real candidate. -/
theorem fastCut_valid {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a ≤ b) (m' : ℝ) (q' w' : Fin n → ℝ) :
    (fastCut a b m q w).eval m' q' w' ≤ lowerMoment a b m' q' w' := by
  let ss := (buildSegments (sourceLines m q w) a b).1
  let f := fun x : ℝ => 2 * envelope m' q' w' x / x ^ 3
  have hb (s : Segment) (hs : s ∈ ss) :=
    segments_bounds (buildStack (sourceLines m q w)).1 a b hab hs
  have hint (s : Segment) (hs : s ∈ ss) :
      IntervalIntegrable f volume (s.lo : ℝ) (s.hi : ℝ) := by
    apply ContinuousOn.intervalIntegrable
    rw [uIcc_of_le (by exact_mod_cast (hb s hs).2.1)]
    exact weighted_continuousOn (by exact_mod_cast ha.trans_le (hb s hs).1)
      (envelope_continuous m' q' w')
  have hpoint (s : Segment) (hs : s ∈ ss) :
      (segmentForm (sourceIndex m q w s.active) s.lo s.hi).eval m' q' w' ≤
      ∫ x in (s.lo : ℝ)..(s.hi : ℝ), f x := by
    rw [segmentForm_eval_eq_integral _ (ha.trans_le (hb s hs).1) (hb s hs).2.1]
    have ho : (s.lo : ℝ) ≤ s.hi := by exact_mod_cast (hb s hs).2.1
    have hp : (0 : ℝ) < s.lo := by exact_mod_cast ha.trans_le (hb s hs).1
    have hl : IntervalIntegrable
        (fun x => 2 * line m' q' w' (sourceIndex m q w s.active) x / x ^ 3)
        volume (s.lo : ℝ) (s.hi : ℝ) := by
      apply ContinuousOn.intervalIntegrable
      rw [uIcc_of_le ho]
      exact weighted_continuousOn hp (line_continuous m' q' w' _)
    apply intervalIntegral.integral_mono_on ho hl (hint s hs)
    intro x hx
    exact div_le_div_of_nonneg_right
      (mul_le_mul_of_nonneg_left (line_le_envelope m' q' w' _ x) (by norm_num))
      (pow_nonneg (hp.trans_le hx.1).le 3)
  have hc : Chain a b ss := segments_chain _ (buildStack_nonempty _ (by
    intro he
    have hz := sourceLines_zero m q w
    rw [he] at hz
    exact List.not_mem_nil hz)) a b
  have hsum : (ss.map fun s =>
      (segmentForm (sourceIndex m q w s.active) s.lo s.hi).eval m' q' w').sum ≤
      (ss.map fun s => ∫ x in (s.lo : ℝ)..(s.hi : ℝ), f x).sum := by
    exact List.sum_le_sum hpoint
  rw [hc.sum_integral hint] at hsum
  unfold fastCut lowerMoment
  rw [RationalAffineForm.eval_add, RationalAffineForm_eval_list_sum, List.map_map]
  simp only [Function.comp_def]
  have hbase : RationalAffineForm.eval
      ((1 / a + a / a ^ 2, -(1 / a ^ 2), 0, 0) : RationalAffineForm n) m' q' w' =
      1 / (a : ℝ) - (m' - a) / (a : ℝ) ^ 2 := by
    simp [RationalAffineForm.eval]
    ring
  rw [hbase]
  exact add_le_add_right hsum _

/-- Extraction returns a strict separating rational cut on every violated lower bound. -/
theorem fastCut_separates {n : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a ≤ b) (ht : t < fastLowerMoment a b m q w) :
    (t : ℝ) < (fastCut a b m q w).eval m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ∧
    ∀ m' q' w', (fastCut a b m q w).eval m' q' w' ≤ lowerMoment a b m' q' w' := by
  constructor
  · rw [fastCut_exact ha hab]
    exact_mod_cast ht
  · exact fastCut_valid ha hab

/-- Actual source-line equality tests used in the extraction stage. -/
def fastCutLookupCharge {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) : ℕ :=
  (((buildSegments (sourceLines m q w) a b).1).map fun s =>
    (lookupSource (sourceLine m q w) s.active (List.finRange (2 * n + 2))).2).sum

/-- Linear search per segment adds at most a quadratic number of line comparisons. -/
theorem fastCutLookupCharge_le {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) :
    fastCutLookupCharge a b m q w ≤ (2 * n + 2) ^ 2 := by
  let ss := (buildSegments (sourceLines m q w) a b).1
  have hlen : ss.length ≤ 2 * n + 2 := by
    simpa only [ss, sourceLines, List.length_ofFn] using
      buildSegments_length (sourceLines m q w) a b
  have hc : (ss.map fun s =>
      (lookupSource (sourceLine m q w) s.active (List.finRange (2 * n + 2))).2).sum ≤
      (ss.map fun _ => 2 * n + 2).sum := by
    apply List.sum_le_sum
    intro s _
    simpa only [List.length_finRange] using
      lookupSource_cost (sourceLine m q w) s.active (List.finRange (2 * n + 2))
  simp only [List.map_const', List.sum_replicate, smul_eq_mul] at hc
  change _ ≤ _
  change fastCutLookupCharge a b m q w ≤ _ at hc
  nlinarith

/-- Arithmetic charge for producing and materializing the coefficient vector.
Each lookup visit has a charge of eight: at most four arithmetic operations to
form the source line and two rational comparisons, with spare capacity. Each
segment has a charge of `100*(n+1)` for its two endpoint factors, signs, and the
`2*n+2` coefficient additions. The extra block covers the tangent and source
construction. This is an arithmetic charge; rational bit sizes are bounded
separately. -/
def fastCutArithmeticCharge {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) : ℕ :=
  (buildSegments (sourceLines m q w) a b).2 + 8 * fastCutLookupCharge a b m q w +
    100 * (n + 1) * ((buildSegments (sourceLines m q w) a b).1.length + 1)

/-- The complete extraction has polynomial arithmetic charge; the envelope stage
retains its sharper `O(N log N)` bound. -/
theorem fastCutArithmeticCharge_le {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) :
    fastCutArithmeticCharge a b m q w ≤
      (2 * n + 2) * ((2 * n + 2).log2 + 37) + 8 * (2 * n + 2) ^ 2 +
        100 * (n + 1) * (2 * n + 3) := by
  have hb := buildSegments_cost (sourceLines m q w) a b
  have hl := buildSegments_length (sourceLines m q w) a b
  simp only [sourceLines, List.length_ofFn] at hb hl
  have hlookup := fastCutLookupCharge_le a b m q w
  have hlen : (buildSegments (sourceLines m q w) a b).1.length + 1 ≤ 2 * n + 3 := by
    change (buildSegments (sourceLines m q w) a b).1.length ≤ 2 * n + 2 at hl
    omega
  exact add_le_add (add_le_add hb (Nat.mul_le_mul_left 8 hlookup))
    (Nat.mul_le_mul_left (100 * (n + 1)) hlen)

end ReciprocalAnchor.ManyLeaf.FastEnvelope
