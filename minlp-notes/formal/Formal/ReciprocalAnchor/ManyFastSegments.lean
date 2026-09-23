import Formal.ReciprocalAnchor.ManyFastConstruction

namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

structure Segment where
  lo : ℚ
  hi : ℚ
  active : Line
  deriving Repr

/-- Clip the ordered envelope intervals to `[lo,hi]`, emitting from right to left. -/
def segments : List Line → ℚ → ℚ → List Segment
  | [], _, _ => []
  | [c], lo, hi => [⟨lo, hi, c⟩]
  | c :: d :: rest, lo, hi =>
      let t := cross d c
      if t ≤ lo then [⟨lo, hi, c⟩]
      else if hi ≤ t then segments (d :: rest) lo hi
      else ⟨t, hi, c⟩ :: segments (d :: rest) lo t

theorem segments_length (stack : List Line) (lo hi : ℚ) :
    (segments stack lo hi).length ≤ stack.length := by
  induction stack, lo, hi using segments.induct with
  | case1 => simp [segments]
  | case2 c lo hi => simp [segments]
  | case3 c d rest lo hi t h =>
    dsimp only [t] at *
    simp [segments, h]
  | case4 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte]
    simp only [List.length_cons] at *
    omega
  | case5 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte, List.length_cons]
    simp only [List.length_cons] at ih
    omega

theorem reverse_eval_le_iff_real {a b : Line} (hab : a.slope < b.slope) (x : ℝ) :
    b.evalReal x ≤ a.evalReal x ↔ x ≤ (cross a b : ℝ) := by
  have hd : 0 < (b.slope : ℝ) - a.slope := by exact_mod_cast sub_pos.mpr hab
  simp only [cross, Rat.cast_div, Rat.cast_sub]
  rw [le_div_iff₀ hd]
  dsimp [Line.evalReal]
  constructor <;> intro h <;> nlinarith

/-- Each emitted interval lies within the requested range and has a retained active line. -/
theorem segments_bounds (stack : List Line) (lo hi : ℚ) (hlo : lo ≤ hi)
    {s : Segment} (hs : s ∈ segments stack lo hi) :
    lo ≤ s.lo ∧ s.lo ≤ s.hi ∧ s.hi ≤ hi ∧ s.active ∈ stack := by
  induction stack, lo, hi using segments.induct with
  | case1 => simp [segments] at hs
  | case2 c lo hi =>
    simp only [segments, List.mem_singleton] at hs
    subst s
    exact ⟨le_rfl, hlo, le_rfl, by simp⟩
  | case3 c d rest lo hi t h =>
    dsimp only [t] at *
    simp only [segments, h, ↓reduceIte, List.mem_singleton] at hs
    subst s
    exact ⟨le_rfl, hlo, le_rfl, by simp⟩
  | case4 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte] at hs
    obtain ⟨ha, hb, hc, hd⟩ := ih hlo hs
    exact ⟨ha, hb, hc, List.mem_cons_of_mem _ hd⟩
  | case5 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte, List.mem_cons] at hs
    rcases hs with he | hs
    · subst s
      exact ⟨(lt_of_not_ge h).le, (lt_of_not_ge h').le, le_rfl, by simp⟩
    · obtain ⟨ha, hb, hc, hd⟩ := ih (lt_of_not_ge h).le hs
      exact ⟨ha, hb, hc.trans (lt_of_not_ge h').le, List.mem_cons_of_mem _ hd⟩

/-- Every point in each emitted interval is dominated by its active line. -/
theorem segments_active (stack : List Line) (lo hi : ℚ) (hg : Good stack) (hlo : lo ≤ hi)
    {s : Segment} (hs : s ∈ segments stack lo hi) (x : ℝ)
    (hx : (s.lo : ℝ) ≤ x ∧ x ≤ (s.hi : ℝ)) :
    ∀ l ∈ stack, l.evalReal x ≤ s.active.evalReal x := by
  induction stack, lo, hi using segments.induct with
  | case1 => simp [segments] at hs
  | case2 c lo hi =>
    simp only [segments, List.mem_singleton] at hs
    subst s
    intro l hl
    simp only [List.mem_singleton] at hl
    subst l
    exact le_rfl
  | case3 c d rest lo hi t h =>
    dsimp only [t] at *
    simp only [segments, h, ↓reduceIte, List.mem_singleton] at hs
    subst s
    have ht : (cross d c : ℝ) ≤ x := (by exact_mod_cast h : (cross d c : ℝ) ≤ lo).trans hx.1
    intro l hl
    rcases List.mem_cons.mp hl with he | hl
    · subst l; exact le_rfl
    · exact head_dominates hg x ht l hl
  | case4 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte] at hs
    have htail := ih (good_tail c _ hg) hlo hs
    have hsi := segments_bounds (d :: rest) lo hi hlo hs
    have hxt : x ≤ (cross d c : ℝ) :=
      hx.2.trans ((by exact_mod_cast hsi.2.2.1 : (s.hi : ℝ) ≤ hi).trans
        (by exact_mod_cast h'))
    intro l hl
    rcases List.mem_cons.mp hl with he | hl
    · subst l
      exact ((reverse_eval_le_iff_real (good_pair_slope hg) x).2 hxt).trans
        (htail d (by simp))
    · exact htail l hl
  | case5 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte, List.mem_cons] at hs
    rcases hs with he | hs
    · subst s
      intro l hl
      rcases List.mem_cons.mp hl with he | hl
      · subst l; exact le_rfl
      · exact head_dominates hg x hx.1 l hl
    · have htail := ih (good_tail c _ hg) (lt_of_not_ge h).le hs
      have hsi := segments_bounds (d :: rest) lo (cross d c) (lt_of_not_ge h).le hs
      have hxt : x ≤ (cross d c : ℝ) := hx.2.trans (by exact_mod_cast hsi.2.2.1)
      intro l hl
      rcases List.mem_cons.mp hl with he | hl
      · subst l
        exact ((reverse_eval_le_iff_real (good_pair_slope hg) x).2 hxt).trans
          (htail d (by simp))
      · exact htail l hl

/-- Endpoint adjacency for the emitted right-to-left partition. -/
def Chain (lo : ℚ) : ℚ → List Segment → Prop
  | hi, [] => hi = lo
  | hi, s :: rest => s.hi = hi ∧ Chain lo s.lo rest

theorem segments_chain (stack : List Line) (hne : stack ≠ []) (lo hi : ℚ) :
    Chain lo hi (segments stack lo hi) := by
  induction stack, lo, hi using segments.induct with
  | case1 => contradiction
  | case2 c lo hi => simp [segments, Chain]
  | case3 c d rest lo hi t h =>
    dsimp only [t] at *
    simp [segments, h, Chain]
  | case4 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte]
    exact ih (by simp)
  | case5 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte, Chain]
    exact ⟨trivial, ih (by simp)⟩

/-- A cost semantics for clipping: each visited nonterminal position performs
three rational operations for its intersection and at most two comparisons. -/
def segmentsCharge : List Line → ℚ → ℚ → ℕ
  | [], _, _ => 0
  | [_], _, _ => 0
  | c :: d :: rest, lo, hi =>
      let t := cross d c
      if t ≤ lo then 5
      else if hi ≤ t then 5 + segmentsCharge (d :: rest) lo hi
      else 5 + segmentsCharge (d :: rest) lo t

theorem segmentsCharge_le (stack : List Line) (lo hi : ℚ) :
    segmentsCharge stack lo hi ≤ 5 * stack.length := by
  induction stack, lo, hi using segments.induct with
  | case1 => simp [segmentsCharge]
  | case2 c lo hi => simp [segmentsCharge]
  | case3 c d rest lo hi t h =>
    dsimp only [t] at *
    simp [segmentsCharge, h]
  | case4 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segmentsCharge, h, h', ↓reduceIte, List.length_cons] at *
    omega
  | case5 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segmentsCharge, h, h', ↓reduceIte, List.length_cons] at *
    omega

/-- Every produced rational knot is an original endpoint or an input-line intersection. -/
def SourceKnot (source : List Line) (a b t : ℚ) : Prop :=
  t = a ∨ t = b ∨ ∃ u ∈ source, ∃ v ∈ source, t = cross u v

theorem segments_knots (source stack : List Line) (a b lo hi : ℚ)
    (hsub : ∀ l ∈ stack, l ∈ source)
    (hl : SourceKnot source a b lo) (hh : SourceKnot source a b hi)
    {s : Segment} (hs : s ∈ segments stack lo hi) :
    SourceKnot source a b s.lo ∧ SourceKnot source a b s.hi := by
  induction stack, lo, hi using segments.induct with
  | case1 => simp [segments] at hs
  | case2 c lo hi =>
    simp only [segments, List.mem_singleton] at hs
    subst s
    exact ⟨hl, hh⟩
  | case3 c d rest lo hi t h =>
    dsimp only [t] at *
    simp only [segments, h, ↓reduceIte, List.mem_singleton] at hs
    subst s
    exact ⟨hl, hh⟩
  | case4 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte] at hs
    exact ih (fun l hm => hsub l (List.mem_cons_of_mem _ hm)) hl hh hs
  | case5 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    have ht : SourceKnot source a b (cross d c) :=
      Or.inr (Or.inr ⟨d, hsub d (by simp), c, hsub c (by simp), rfl⟩)
    simp only [segments, h, h', ↓reduceIte, List.mem_cons] at hs
    rcases hs with he | hs
    · subst s; exact ⟨ht, hh⟩
    · exact ih (fun l hm => hsub l (List.mem_cons_of_mem _ hm)) hl ht hs

/-- The full rational upper-envelope construction, including clipping to the box.
The charge includes both clipping and the separate traversal computing its charge. -/
def buildSegments (input : List Line) (a b : ℚ) : List Segment × ℕ :=
  let stack := buildStack input
  (segments stack.1 a b, stack.2 + 2 * segmentsCharge stack.1 a b)

theorem buildSegments_length (input : List Line) (a b : ℚ) :
    (buildSegments input a b).1.length ≤ input.length :=
  (segments_length _ a b).trans (buildStack_length input)

theorem buildSegments_cost (input : List Line) (a b : ℚ) :
    (buildSegments input a b).2 ≤ input.length * (input.length.log2 + 37) := by
  have hs := buildStack_cost input
  have hl := buildStack_length input
  have hc := segmentsCharge_le (buildStack input).1 a b
  dsimp [buildSegments]
  nlinarith

end ReciprocalAnchor.ManyLeaf.FastEnvelope
