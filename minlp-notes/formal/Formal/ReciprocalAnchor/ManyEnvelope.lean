import Mathlib

/-! A finite affine envelope has an actual finite partition into input lines. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators
variable {𝕜 : Type*} [Field 𝕜] [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜]

noncomputable def affineEnvelope {ι : Type*} [Fintype ι] [Nonempty ι]
    (c d : ι → 𝕜) (s : 𝕜) : 𝕜 :=
  Finset.univ.sup' Finset.univ_nonempty (fun i => c i + d i * s)

omit [IsStrictOrderedRing 𝕜] in
theorem affine_le_envelope {ι : Type*} [Fintype ι] [Nonempty ι]
    (c d : ι → 𝕜) (i : ι) (s : 𝕜) : c i + d i * s ≤ affineEnvelope c d s := by
  exact Finset.le_sup' (fun j => c j + d j * s) (Finset.mem_univ i)

omit [IsStrictOrderedRing 𝕜] in
theorem affineEnvelope_eq_iff {ι : Type*} [Fintype ι] [Nonempty ι]
    (c d : ι → 𝕜) (i : ι) (s : 𝕜) :
    affineEnvelope c d s = c i + d i * s ↔ ∀ j, c j + d j * s ≤ c i + d i * s := by
  constructor
  · intro h j
    rw [← h]
    exact affine_le_envelope c d j s
  · intro h
    apply le_antisymm (Finset.sup'_le _ _ (by simpa using h))
    exact affine_le_envelope c d i s

/-- An affine difference cannot change sign inside an interval with no intersection. -/
theorem affine_nonnegative_of_no_root {v e l r t s : 𝕜}
    (hlt : l < t) (htr : t < r) (hls : l ≤ s) (hsr : s ≤ r)
    (ht : 0 ≤ v + e * t)
    (hroot : e ≠ 0 → ¬ l < -v / e ∨ ¬ -v / e < r) :
    0 ≤ v + e * s := by
  by_cases he : e = 0
  · simpa [he] using ht
  have hz : e * (-v / e) = -v := by field_simp
  rcases hroot he with hzleft | hzright
  · have hzle : -v / e ≤ l := le_of_not_gt hzleft
    rcases lt_or_gt_of_ne he with hneg | hpos
    · nlinarith [mul_neg_of_neg_of_pos hneg (sub_pos.mpr (lt_of_le_of_lt hzle hlt))]
    · nlinarith [mul_nonneg (le_of_lt hpos) (sub_nonneg.mpr (le_trans hzle hls))]
  · have hzge : r ≤ -v / e := le_of_not_gt hzright
    rcases lt_or_gt_of_ne he with hneg | hpos
    · nlinarith [mul_nonneg (le_of_lt (neg_pos.mpr hneg))
        (sub_nonneg.mpr (le_trans hsr hzge))]
    · nlinarith [mul_pos hpos (sub_pos.mpr (lt_of_lt_of_le htr hzge))]

/-- Every interval containing no proper line intersection has a single active line. -/
theorem exists_active_on_interval {ι : Type*} [Fintype ι] [Nonempty ι]
    (c d : ι → 𝕜) {l r : 𝕜} (hlr : l < r)
    (hcross : ∀ i j, d i ≠ d j →
      ¬ l < (c j - c i) / (d i - d j) ∨ ¬ (c j - c i) / (d i - d j) < r) :
    ∃ i, ∀ s ∈ Set.Icc l r, affineEnvelope c d s = c i + d i * s := by
  obtain ⟨i, _, hi⟩ := Finset.exists_mem_eq_sup' Finset.univ_nonempty
    (fun i => c i + d i * ((l + r) / 2))
  refine ⟨i, ?_⟩
  intro s hs
  apply (affineEnvelope_eq_iff c d i s).mpr
  intro j
  have ht : 0 ≤ (c i - c j) + (d i - d j) * ((l + r) / 2) := by
    have := affine_le_envelope c d j ((l + r) / 2)
    change _ ≤ Finset.univ.sup' _ _ at this
    rw [hi] at this
    nlinarith
  have h := affine_nonnegative_of_no_root (by linarith : l < (l + r) / 2)
    (by linarith : (l + r) / 2 < r) hs.1 hs.2 ht (by
      intro he
      have hd : d i ≠ d j := sub_ne_zero.mp he
      simpa only [neg_sub] using hcross i j hd)
  nlinarith

/-- Active affine pieces have nondecreasing slopes. -/
theorem active_slopes_ordered {ι : Type*} [Fintype ι] [Nonempty ι]
    (c d : ι → 𝕜) {i j : ι} {s t : 𝕜} (hst : s < t)
    (hi : affineEnvelope c d s = c i + d i * s)
    (hj : affineEnvelope c d t = c j + d j * t) : d i ≤ d j := by
  have h1 := (affineEnvelope_eq_iff c d i s).mp hi j
  have h2 := (affineEnvelope_eq_iff c d j t).mp hj i
  nlinarith

/-- A genuine partition, with each cell assigned one of the original lines. -/
structure AffinePartition {ι : Type*} [Fintype ι] [Nonempty ι]
    (c d : ι → 𝕜) (a b : 𝕜) where
  size : ℕ
  pos : 0 < size
  knot : Fin (size + 1) → 𝕜
  strict : StrictMono knot
  first : knot 0 = a
  last : knot (Fin.last size) = b
  active : Fin size → ι
  agrees : ∀ i s, s ∈ Set.Icc (knot i.castSucc) (knot i.succ) →
    affineEnvelope c d s = c (active i) + d (active i) * s

theorem AffinePartition.covers {ι : Type*} [Fintype ι] [Nonempty ι]
    {c d : ι → 𝕜} {a b : 𝕜} (P : AffinePartition c d a b)
    {s : 𝕜} (hs : s ∈ Set.Icc a b) :
    ∃ i : Fin P.size, s ∈ Set.Icc (P.knot i.castSucc) (P.knot i.succ) := by
  classical
  by_cases hsb : s = b
  · let i : Fin P.size := ⟨P.size - 1, by have := P.pos; omega⟩
    have hilast : i.succ = Fin.last P.size := by ext; dsimp [i]; have := P.pos; omega
    refine ⟨i, ?_, ?_⟩
    · simpa only [P.last, hsb] using P.strict.monotone (Fin.le_last i.castSucc)
    · rw [hsb, hilast, P.last]
  have hslt : s < b := lt_of_le_of_ne hs.2 hsb
  let S : Finset (Fin (P.size + 1)) := Finset.univ.filter (fun i => P.knot i ≤ s)
  have hzero : (0 : Fin (P.size + 1)) ∈ S := by simp [S, P.first, hs.1]
  obtain ⟨j, hj, hmax⟩ := Finset.exists_max_image S (fun i => i.val) ⟨0, hzero⟩
  have hjs : P.knot j ≤ s := (Finset.mem_filter.mp hj).2
  have hjlt : j.val < P.size := by
    by_contra h
    have heq : j = Fin.last P.size := by ext; have := j.isLt; simp; omega
    rw [heq, P.last] at hjs
    linarith
  let i : Fin P.size := ⟨j.val, hjlt⟩
  have hij : i.castSucc = j := by ext; rfl
  refine ⟨i, by simpa [hij] using hjs, ?_⟩
  by_contra h
  have hmem : i.succ ∈ S := Finset.mem_filter.mpr
    ⟨Finset.mem_univ _, (lt_of_not_ge h).le⟩
  have := hmax _ hmem
  dsimp [i] at this
  omega

omit [Field 𝕜] [IsStrictOrderedRing 𝕜] in
/-- Adjacent elements of an ordered finite set leave no member between them. -/
theorem orderEmbOfFin_no_between (S : Finset 𝕜) {N : ℕ} (hcard : S.card = N + 1)
    (i : Fin N) {s : 𝕜} (hs : s ∈ S) :
    ¬ S.orderEmbOfFin hcard i.castSucc < s ∨
      ¬ s < S.orderEmbOfFin hcard i.succ := by
  have hr : s ∈ Set.range (S.orderEmbOfFin hcard) := by
    rw [Finset.range_orderEmbOfFin]
    exact hs
  obtain ⟨j, rfl⟩ := hr
  by_cases h : S.orderEmbOfFin hcard i.castSucc < S.orderEmbOfFin hcard j
  · right
    intro h'
    have h1 := (S.orderEmbOfFin hcard).lt_iff_lt.mp h
    have h2 := (S.orderEmbOfFin hcard).lt_iff_lt.mp h'
    have : i.val < j.val := h1
    have : j.val < i.val + 1 := h2
    omega
  · exact Or.inl h

/-- The construction uses all pair intersections. It requires no proposed partition. -/
theorem exists_affinePartition_with_provenance {ι : Type*} [Fintype ι] [Nonempty ι]
    (c d : ι → 𝕜) {a b : 𝕜} (hab : a < b) :
    ∃ P : AffinePartition c d a b,
      (∀ i, P.knot i = a ∨ P.knot i = b ∨
        ∃ j k, P.knot i = (c k - c j) / (d j - d k)) ∧
      P.size ≤ Fintype.card ι ^ 2 + 1 := by
  classical
  let roots : Finset 𝕜 := Finset.univ.image
    (fun ij : ι × ι => (c ij.2 - c ij.1) / (d ij.1 - d ij.2))
  let S : Finset 𝕜 := (insert a (insert b roots)).filter (fun s => a ≤ s ∧ s ≤ b)
  have ha : a ∈ S := by simp [S, hab.le]
  have hb : b ∈ S := by simp [S, hab.le]
  have hbds : ∀ s ∈ S, a ≤ s ∧ s ≤ b := by
    intro s hs
    exact (Finset.mem_filter.mp hs).2
  have htwo : 2 ≤ S.card := by
    have hsub : ({a, b} : Finset 𝕜) ⊆ S := by
      intro x hx
      simp only [Finset.mem_insert, Finset.mem_singleton] at hx
      rcases hx with rfl | rfl <;> assumption
    have := Finset.card_le_card hsub
    simpa [hab.ne] using this
  obtain ⟨N, hN⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : S.card ≠ 0)
  have hcard : S.card = N + 1 := hN
  let knot := S.orderEmbOfFin hcard
  have hknot : ∀ i, knot i ∈ S := S.orderEmbOfFin_mem hcard
  have hfirst : knot 0 = a := by
    apply le_antisymm
    · have har : a ∈ Set.range knot := by
        dsimp [knot]
        rw [Finset.range_orderEmbOfFin]
        exact ha
      obtain ⟨j, hj⟩ := har
      rw [← hj]
      exact knot.monotone (Fin.zero_le j)
    · exact (hbds _ (hknot 0)).1
  have hlast : knot (Fin.last N) = b := by
    apply le_antisymm
    · exact (hbds _ (hknot (Fin.last N))).2
    · have hbr : b ∈ Set.range knot := by
        dsimp [knot]
        rw [Finset.range_orderEmbOfFin]
        exact hb
      obtain ⟨j, hj⟩ := hbr
      rw [← hj]
      exact knot.monotone (Fin.le_last j)
  have hex : ∀ i : Fin N, ∃ j, ∀ s ∈ Set.Icc (knot i.castSucc) (knot i.succ),
      affineEnvelope c d s = c j + d j * s := by
    intro i
    apply exists_active_on_interval c d (knot.strictMono (by simp))
    intro j k _
    by_cases hr : a ≤ (c k - c j) / (d j - d k) ∧
        (c k - c j) / (d j - d k) ≤ b
    · apply orderEmbOfFin_no_between S hcard i
      apply Finset.mem_filter.mpr
      refine ⟨Finset.mem_insert_of_mem (Finset.mem_insert_of_mem ?_), hr⟩
      exact Finset.mem_image.mpr ⟨(j, k), Finset.mem_univ _, rfl⟩
    · by_cases hleft : a ≤ (c k - c j) / (d j - d k)
      · right
        have := (hbds _ (hknot i.succ)).2
        have : b < (c k - c j) / (d j - d k) := lt_of_not_ge (fun h => hr ⟨hleft, h⟩)
        linarith
      · left
        have := (hbds _ (hknot i.castSucc)).1
        linarith
  choose active hagrees using hex
  let P : AffinePartition c d a b :=
    ⟨N, by omega, knot, knot.strictMono, hfirst, hlast, active, hagrees⟩
  refine ⟨P, ?_, ?_⟩
  · intro i
    have h := (Finset.mem_filter.mp (hknot i)).1
    rcases Finset.mem_insert.mp h with h | h
    · exact Or.inl h
    rcases Finset.mem_insert.mp h with h | h
    · exact Or.inr (Or.inl h)
    obtain ⟨⟨j, k⟩, _, hjk⟩ := Finset.mem_image.mp h
    exact Or.inr (Or.inr ⟨j, k, hjk.symm⟩)
  · have h1 : S.card ≤ (insert a (insert b roots)).card := Finset.card_filter_le _ _
    have h2 := Finset.card_insert_le a (insert b roots)
    have h3 := Finset.card_insert_le b roots
    have h4 : roots.card ≤ Fintype.card (ι × ι) := by
      simpa only [Finset.card_univ] using
        (Finset.card_image_le (s := (Finset.univ : Finset (ι × ι)))
          (f := fun ij : ι × ι => (c ij.2 - c ij.1) / (d ij.1 - d ij.2)))
    simp only [Fintype.card_prod] at h4
    change N ≤ Fintype.card ι ^ 2 + 1
    nlinarith

/-- A finite affine envelope admits an actual partition into input lines. -/
theorem exists_affinePartition {ι : Type*} [Fintype ι] [Nonempty ι]
    (c d : ι → 𝕜) {a b : 𝕜} (hab : a < b) :
    Nonempty (AffinePartition c d a b) := by
  obtain ⟨P, _, _⟩ := exists_affinePartition_with_provenance c d hab
  exact ⟨P⟩

end ReciprocalAnchor.ManyLeaf
