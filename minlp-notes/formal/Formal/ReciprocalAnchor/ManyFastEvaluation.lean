import Formal.ReciprocalAnchor.ManyFastDominance
import Formal.ReciprocalAnchor.ManyGeometry
import Formal.ReciprocalAnchor.ManyAlgorithm

namespace ReciprocalAnchor.ManyLeaf.FastEnvelope
open MeasureTheory Set

/-- Exact arithmetic evaluation of a produced segment. -/
def Segment.integral (s : Segment) : ℚ :=
  rationalSegmentIntegral ⟨s.active.intercept, -s.active.slope⟩ s.lo s.hi

theorem Segment.integral_eq (s : Segment) (hlo : 0 < s.lo) (horder : s.lo ≤ s.hi) :
    (s.integral : ℝ) = ∫ x in (s.lo : ℝ)..(s.hi : ℝ), 2 * s.active.evalReal x / x ^ 3 := by
  rw [Segment.integral, cast_rationalSegmentIntegral,
    ← affine_call_integral (by exact_mod_cast hlo) (by exact_mod_cast horder)]
  apply intervalIntegral.integral_congr
  intro x _
  dsimp only [Line.evalReal]
  push_cast
  ring

/-- A chain of segments partitions the integral, including zero-length pieces. -/
theorem Chain.sum_integral {ss : List Segment} {a b : ℚ} {f : ℝ → ℝ}
    (hc : Chain a b ss)
    (hi : ∀ s ∈ ss, IntervalIntegrable f volume (s.lo : ℝ) (s.hi : ℝ)) :
    ((ss.map fun s => ∫ x in (s.lo : ℝ)..(s.hi : ℝ), f x).sum) =
      ∫ x in (a : ℝ)..(b : ℝ), f x := by
  induction ss generalizing b with
  | nil =>
    change b = a at hc
    subst b
    simp
  | cons s rest ih =>
    obtain ⟨hs, hc⟩ := hc
    subst b
    simp only [List.map_cons, List.sum_cons]
    rw [ih hc (fun t ht => hi t (List.mem_cons_of_mem _ ht))]
    have hr : IntervalIntegrable f volume (a : ℝ) (s.lo : ℝ) := by
      clear ih
      induction rest generalizing s with
      | nil =>
        change s.lo = a at hc
        rw [hc]
      | cons t ts ih =>
        obtain ⟨ht, hts⟩ := hc
        have htI := hi t (by simp)
        have htail : IntervalIntegrable f volume (a : ℝ) (t.lo : ℝ) :=
          ih t (fun u hu => hi u (List.mem_cons_of_mem _ hu)) hts
        rw [← ht]
        exact htail.trans htI
    rw [add_comm]
    exact intervalIntegral.integral_add_adjacent_intervals hr (hi s (by simp))

/-- The source lines, with their ordinary signed slope. -/
def sourceLines {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) : List Line :=
  List.ofFn (fun i : Fin (2 * n + 2) =>
    ⟨-(rationalLines m q w i).negSlope, (rationalLines m q w i).intercept⟩)

theorem sourceLine_eval {n : ℕ} (m : ℚ) (q w : Fin n → ℚ)
    (i : Fin (2 * n + 2)) (x : ℝ) :
    (⟨-(rationalLines m q w i).negSlope, (rationalLines m q w i).intercept⟩ : Line).evalReal x =
      line (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) i x := by
  rw [← rationalLines_evalReal]
  simp [Line.evalReal, RationalLine.evalReal, sub_eq_add_neg]

theorem sourceLines_zero {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) :
    (⟨0, 0⟩ : Line) ∈ sourceLines m q w := by
  apply List.mem_ofFn.mpr
  refine ⟨⟨2 * n, by omega⟩, ?_⟩
  simp [rationalLines, show ¬ 2 * n < n by omega]

theorem sourceLines_valueReal {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) (x : ℝ) :
    valueReal (sourceLines m q w) x =
      envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) x := by
  apply le_antisymm
  · apply valueReal_le (envelope_nonneg _ _ _ _)
    intro l hl
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hl
    rw [sourceLine_eval]
    exact line_le_envelope _ _ _ _ _
  · apply envelope_le
    intro i
    rw [← sourceLine_eval]
    exact evalReal_le_valueReal (ls := sourceLines m q w)
      (List.mem_ofFn.mpr ⟨i, rfl⟩) x

/-- Evaluate the actual fast envelope output with exact rational segment integrals. -/
def fastLowerMoment {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) : ℚ :=
  1 / a - (m - a) / a ^ 2 +
    (((buildSegments (sourceLines m q w) a b).1).map Segment.integral).sum

/-- Correctness of the executable slope-sort/stack evaluator on every rational input. -/
theorem fastLowerMoment_eq {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a ≤ b) :
    (fastLowerMoment a b m q w : ℝ) =
      lowerMoment a b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) := by
  let ss := (buildSegments (sourceLines m q w) a b).1
  let f := fun x : ℝ =>
    2 * envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) x / x ^ 3
  have hbounds (s : Segment) (hs : s ∈ ss) := segments_bounds
    (buildStack (sourceLines m q w)).1 a b hab hs
  have hactive (s : Segment) (hs : s ∈ ss) (x : ℝ)
      (hx : (s.lo : ℝ) ≤ x ∧ x ≤ (s.hi : ℝ)) :
      envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) x = s.active.evalReal x := by
    rw [← sourceLines_valueReal]
    exact built_segments_valueReal _ _ _ hab (sourceLines_zero m q w) hs x hx
  have hne : sourceLines m q w ≠ [] := by
    intro he
    have hz := sourceLines_zero m q w
    rw [he] at hz
    exact List.not_mem_nil hz
  have hc : Chain a b ss := segments_chain _ (buildStack_nonempty _ hne) a b
  have hint (s : Segment) (hs : s ∈ ss) :
      IntervalIntegrable f volume (s.lo : ℝ) (s.hi : ℝ) := by
    have hp : 0 < (s.lo : ℝ) := by exact_mod_cast ha.trans_le (hbounds s hs).1
    have ho : (s.lo : ℝ) ≤ s.hi := by exact_mod_cast (hbounds s hs).2.1
    apply ContinuousOn.intervalIntegrable
    rw [uIcc_of_le ho]
    have he : ContinuousOn
        (envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)))
        (Icc (s.lo : ℝ) (s.hi : ℝ)) :=
      (envelope_continuous _ _ _).continuousOn
    apply ContinuousOn.div (continuousOn_const.mul he) (continuousOn_id.pow 3)
    intro x hx
    exact pow_ne_zero 3 (ne_of_gt (hp.trans_le hx.1))
  have hp (s : Segment) (hs : s ∈ ss) :
      (s.integral : ℝ) = ∫ x in (s.lo : ℝ)..(s.hi : ℝ), f x := by
    rw [s.integral_eq (ha.trans_le (hbounds s hs).1) (hbounds s hs).2.1]
    apply intervalIntegral.integral_congr
    intro x hx
    rw [uIcc_of_le (by exact_mod_cast (hbounds s hs).2.1)] at hx
    dsimp [f]
    rw [hactive s hs x hx]
  unfold fastLowerMoment lowerMoment
  push_cast
  congr 1
  rw [List.map_map]
  have he : ss.map (fun s => (s.integral : ℝ)) =
      ss.map (fun s => ∫ x in (s.lo : ℝ)..(s.hi : ℝ), f x) := by
    apply List.map_congr_left
    exact hp
  change (ss.map (fun s => (s.integral : ℝ))).sum = _
  rw [he]
  exact hc.sum_integral hint

end ReciprocalAnchor.ManyLeaf.FastEnvelope

