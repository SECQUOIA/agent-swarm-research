import Formal.MultilinearGap.PhysicalEnvelope

/-!
# PB10: integrality of the cube slab

Positive-box obligation PB10 names a *geometric* statement: for `u ∈ [0,1]^n`
with mean sum `S = ∑ i, u i`, the slab

`slab u = {y ∈ [0,1]^n : ⌊S⌋ ≤ ∑ i, y i ≤ ⌈S⌉}`

is integral and contains `u`, so an adjacent-count law with means `u` exists.
This module supplies that statement and its proof.

* `slab` and `slabVertices` (the `0/1` points of the slab), `mem_slab_self`
  (the slab contains `u`), `slab_convex`.
* `slab_subset_convexHull_slabVertices`: **integrality** in the form every point
  of the slab is a convex combination of `0/1` points *of the slab*, and the
  resulting identity `convexHull_slabVertices_eq`.  The proof is the constructive
  form of the extreme-point argument: induction on a finite set covering the
  fractional coordinates.  With two fractional coordinates one is raised and the
  other lowered, at equal rates and in both directions, which fixes the
  coordinate sum and exhibits the point as a convex combination of two slab
  points, each with one fractional coordinate fewer.  With a single fractional
  coordinate the sum of the remaining coordinates is an integer `N`, and the two
  slab bounds are consecutive integers, so both are slack and the fractional
  coordinate may be pushed to `0` and to `1` independently.
* `extremePoints_slab_subset`: the equivalent extreme-point form, a corollary.
* `exists_slabLaw` and `exists_adjacentLaw_of_slab`: the promised consequence.
  The second **re-derives** the statement of `exists_adjacentLaw` (at the full
  support `Finset.univ`) from integrality alone: a law with means `u` supported
  on counts `{⌊S⌋, ⌈S⌉}` has expected count `S`, which pins its count
  distribution to weights `1 - (S - ⌊S⌋)` and `S - ⌊S⌋`.

The direct construction `exists_adjacentLaw` in `PhysicalEnvelope` is untouched
and remains the operational route used by PB11: it works for an arbitrary
support `s` and builds the law explicitly.  This module adds the named geometric
statement, which that construction deliberately avoids.
-/

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*} [Fintype I]

/-! ## The slab and its integral points -/

/-- The lower slab bound `⌊S⌋`, for `S = ∑ i, u i` the prescribed mean sum. -/
def slabFloor (u : I → ℝ) : ℕ := countFloor Finset.univ u

/-- The upper slab bound `⌈S⌉`, for `S = ∑ i, u i` the prescribed mean sum. -/
def slabCeil (u : I → ℝ) : ℕ := ⌈meanSum Finset.univ u⌉₊

/-- PB10's polytope: the points of the unit cube whose coordinate sum lies
between `⌊S⌋` and `⌈S⌉`. -/
def slab (u : I → ℝ) : Set (I → ℝ) :=
  {y | y ∈ cube I ∧ (slabFloor u : ℝ) ≤ ∑ i, y i ∧ ∑ i, y i ≤ (slabCeil u : ℝ)}

/-- The integral points of the slab: the `0/1` points it contains. -/
def slabVertices (u : I → ℝ) : Set (I → ℝ) :=
  {y | y ∈ slab u ∧ ∃ v : Vertex I, y = vertexPoint v}

/-- The two slab bounds are ordered. -/
theorem slabFloor_le_slabCeil (u : I → ℝ) : slabFloor u ≤ slabCeil u :=
  Nat.floor_le_ceil _

/-- The two slab bounds are consecutive integers, or equal when `S` is an
integer.  This is the degenerate case in which the slab is a single hyperplane
slice of the cube. -/
theorem slabCeil_le_slabFloor_add_one (u : I → ℝ) : slabCeil u ≤ slabFloor u + 1 :=
  Nat.ceil_le_floor_add_one _

/-- Membership in the slab, unfolded. -/
theorem mem_slab_iff {u y : I → ℝ} :
    y ∈ slab u ↔ y ∈ cube I ∧ (slabFloor u : ℝ) ≤ ∑ i, y i ∧ ∑ i, y i ≤ (slabCeil u : ℝ) :=
  Iff.rfl

/-- PB10, first half: the slab contains its own mean vector `u`. -/
theorem mem_slab_self {u : I → ℝ} (hu : u ∈ cube I) : u ∈ slab u :=
  ⟨hu, countFloor_le hu, Nat.le_ceil _⟩

/-- A binary point lies in the slab exactly when its success count lies between
the two bounds. -/
theorem vertexPoint_mem_slab_iff (u : I → ℝ) (v : Vertex I) :
    vertexPoint v ∈ slab u ↔ slabFloor u ≤ count v ∧ count v ≤ slabCeil u := by
  have hsum : ∑ i, vertexPoint v i = (count v : ℝ) := by
    rw [← countOn_eq_sum Finset.univ v, countOn_univ]
  constructor
  · rintro ⟨-, h1, h2⟩
    rw [hsum] at h1 h2
    exact ⟨by exact_mod_cast h1, by exact_mod_cast h2⟩
  · rintro ⟨h1, h2⟩
    refine ⟨fun i => ?_, ?_, ?_⟩
    · rw [vertexPoint]; split_ifs <;> norm_num
    · rw [hsum]; exact_mod_cast h1
    · rw [hsum]; exact_mod_cast h2

/-- The integral points of the slab are slab points. -/
theorem slabVertices_subset_slab (u : I → ℝ) : slabVertices u ⊆ slab u := fun _ hy => hy.1

/-- A slab point all of whose coordinates are `0` or `1` is an integral point of
the slab. -/
theorem mem_slabVertices_of_integral {u y : I → ℝ} (hy : y ∈ slab u)
    (hint : ∀ i, y i = 0 ∨ y i = 1) : y ∈ slabVertices u := by
  refine ⟨hy, ⟨fun i => if y i = 1 then true else false, funext fun i => ?_⟩⟩
  rcases hint i with h | h <;> simp [vertexPoint, h]

/-- The slab is convex: it is the cube intersected with two half-spaces. -/
theorem slab_convex (u : I → ℝ) : Convex ℝ (slab u) := by
  rintro x ⟨hxc, hxlo, hxhi⟩ y ⟨hyc, hylo, hyhi⟩ p q hp hq hpq
  have hsum : ∑ i, (p • x + q • y) i = p * (∑ i, x i) + q * (∑ i, y i) := by
    simp [Finset.sum_add_distrib, Finset.mul_sum]
  have hk : p * (slabFloor u : ℝ) + q * (slabFloor u : ℝ) = (slabFloor u : ℝ) := by
    rw [← add_mul, hpq, one_mul]
  have hK : p * (slabCeil u : ℝ) + q * (slabCeil u : ℝ) = (slabCeil u : ℝ) := by
    rw [← add_mul, hpq, one_mul]
  refine ⟨fun i => ?_, ?_, ?_⟩
  · have h1 := hxc i
    have h2 := hyc i
    have hlo : 0 ≤ p * x i + q * y i :=
      add_nonneg (mul_nonneg hp h1.1) (mul_nonneg hq h2.1)
    have hhi : p * x i + q * y i ≤ p * 1 + q * 1 :=
      add_le_add (mul_le_mul_of_nonneg_left h1.2 hp) (mul_le_mul_of_nonneg_left h2.2 hq)
    rw [mul_one, mul_one, hpq] at hhi
    exact ⟨by simpa using hlo, by simpa using hhi⟩
  · rw [hsum, ← hk]
    exact add_le_add (mul_le_mul_of_nonneg_left hxlo hp) (mul_le_mul_of_nonneg_left hylo hq)
  · rw [hsum, ← hK]
    exact add_le_add (mul_le_mul_of_nonneg_left hxhi hp) (mul_le_mul_of_nonneg_left hyhi hq)

/-! ## Integrality -/

open scoped Classical in
/-- Move a single coordinate by `c`, leaving every other coordinate alone. -/
private def bump (y : I → ℝ) (i : I) (c : ℝ) : I → ℝ := fun l => y l + if l = i then c else 0

omit [Fintype I] in
private theorem bump_self (y : I → ℝ) (i : I) (c : ℝ) : bump y i c i = y i + c := by
  simp [bump]

omit [Fintype I] in
private theorem bump_of_ne (y : I → ℝ) (i : I) (c : ℝ) {l : I} (h : l ≠ i) :
    bump y i c l = y l := by
  simp [bump, h]

private theorem sum_bump (y : I → ℝ) (i : I) (c : ℝ) :
    ∑ l, bump y i c l = (∑ l, y l) + c := by
  classical
  simp [bump, Finset.sum_add_distrib, Finset.sum_ite_eq']

omit [Fintype I] in
/-- The opposite move on two distinct coordinates: `i` rises by `h`, `j` falls
by `h`. -/
private theorem bump_pair_left (y : I → ℝ) {i j : I} (hij : i ≠ j) (h : ℝ) :
    bump (bump y i h) j (-h) i = y i + h := by
  rw [bump_of_ne _ _ _ hij, bump_self]

omit [Fintype I] in
private theorem bump_pair_right (y : I → ℝ) {i j : I} (hij : i ≠ j) (h : ℝ) :
    bump (bump y i h) j (-h) j = y j - h := by
  rw [bump_self, bump_of_ne _ _ _ (Ne.symm hij)]
  ring

omit [Fintype I] in
private theorem bump_pair_other (y : I → ℝ) (i j : I) (h : ℝ) {l : I} (hli : l ≠ i) (hlj : l ≠ j) :
    bump (bump y i h) j (-h) l = y l := by
  rw [bump_of_ne _ _ _ hlj, bump_of_ne _ _ _ hli]

private theorem sum_bump_pair (y : I → ℝ) (i j : I) (h : ℝ) :
    ∑ l, bump (bump y i h) j (-h) l = ∑ l, y l := by
  rw [sum_bump, sum_bump]
  ring

/-- The opposite move on two coordinates keeps the coordinate sum fixed, so it
stays in the slab as soon as it stays in the cube. -/
private theorem bump_pair_mem_slab {u y : I → ℝ} (hy : y ∈ slab u) {i j : I} (hij : i ≠ j)
    (h : ℝ) (h1 : 0 ≤ y i + h) (h2 : y i + h ≤ 1) (h3 : 0 ≤ y j - h) (h4 : y j - h ≤ 1) :
    bump (bump y i h) j (-h) ∈ slab u := by
  obtain ⟨hcube, hlo, hhi⟩ := hy
  refine ⟨fun l => ?_, ?_, ?_⟩
  · rcases eq_or_ne l i with rfl | hli
    · rw [bump_pair_left y hij h]; exact ⟨h1, h2⟩
    · rcases eq_or_ne l j with rfl | hlj
      · rw [bump_pair_right y hij h]; exact ⟨h3, h4⟩
      · rw [bump_pair_other y i j h hli hlj]; exact hcube l
  · rw [sum_bump_pair]; exact hlo
  · rw [sum_bump_pair]; exact hhi

/-- The engine of integrality: a slab point whose fractional coordinates all lie
in a finite set `s` of size at most `m` is a convex combination of integral slab
points.  The induction is on `m`. -/
private theorem hull_aux (u : I → ℝ) (m : ℕ) :
    ∀ (y : I → ℝ) (s : Finset I), s.card ≤ m → (∀ l ∉ s, y l = 0 ∨ y l = 1) →
      y ∈ slab u → y ∈ convexHull ℝ (slabVertices u) := by
  classical
  induction m with
  | zero =>
    intro y s hcard hout hy
    have hs : s = ∅ := Finset.card_eq_zero.mp (Nat.le_zero.mp hcard)
    subst hs
    exact subset_convexHull ℝ _ (mem_slabVertices_of_integral hy fun i => hout i (by simp))
  | succ m IH =>
    intro y s hcard hout hy
    by_cases hall : ∀ l, y l = 0 ∨ y l = 1
    · exact subset_convexHull ℝ _ (mem_slabVertices_of_integral hy hall)
    obtain ⟨i, hi⟩ := not_forall.mp hall
    have hi0 : y i ≠ 0 := fun h => hi (Or.inl h)
    have hi1 : y i ≠ 1 := fun h => hi (Or.inr h)
    have hiS : i ∈ s := by
      by_contra hns
      rcases hout i hns with h | h
      · exact hi0 h
      · exact hi1 h
    have hic := hy.1 i
    have hilt : 0 < y i := lt_of_le_of_ne hic.1 (Ne.symm hi0)
    have hiut : y i < 1 := lt_of_le_of_ne hic.2 hi1
    by_cases hsingle : ∀ l, l ≠ i → y l = 0 ∨ y l = 1
    · -- Exactly one fractional coordinate: both slab constraints are slack.
      obtain ⟨N, hN⟩ : ∃ N : ℕ, ∑ l ∈ Finset.univ.erase i, y l = (N : ℝ) := by
        refine ⟨((Finset.univ.erase i).filter fun l => y l = 1).card, ?_⟩
        rw [Finset.card_filter, Nat.cast_sum]
        refine Finset.sum_congr rfl fun l hl => ?_
        rcases hsingle l (Finset.ne_of_mem_erase hl) with h | h <;> simp [h]
      have hsplit : ∑ l, y l = y i + (N : ℝ) := by
        rw [← hN, Finset.add_sum_erase _ y (Finset.mem_univ i)]
      have hlo := hy.2.1
      have hhi := hy.2.2
      rw [hsplit] at hlo hhi
      have hkN : slabFloor u ≤ N := by
        have h : (slabFloor u : ℝ) < (N : ℝ) + 1 := by linarith
        have h' : slabFloor u < N + 1 := by exact_mod_cast h
        omega
      have hNK : N + 1 ≤ slabCeil u := by
        have h : (N : ℝ) < (slabCeil u : ℝ) := by linarith
        have h' : N < slabCeil u := by exact_mod_cast h
        omega
      -- the two children, with the fractional coordinate pushed to `0` and to `1`
      have hchild : ∀ c : ℝ, y i + c = 0 ∨ y i + c = 1 →
          (slabFloor u : ℝ) ≤ (∑ l, y l) + c → (∑ l, y l) + c ≤ (slabCeil u : ℝ) →
          bump y i c ∈ slabVertices u := by
        intro c hc hlo' hhi'
        have hint : ∀ l, bump y i c l = 0 ∨ bump y i c l = 1 := by
          intro l
          rcases eq_or_ne l i with rfl | hli
          · rw [bump_self]; exact hc
          · rw [bump_of_ne _ _ _ hli]; exact hsingle l hli
        refine mem_slabVertices_of_integral ⟨fun l => ?_, ?_, ?_⟩ hint
        · rcases hint l with h | h
          · rw [h]; norm_num
          · rw [h]; norm_num
        · rw [sum_bump]; exact hlo'
        · rw [sum_bump]; exact hhi'
      have hzero : bump y i (-y i) ∈ slabVertices u := by
        refine hchild (-y i) (Or.inl (by ring)) ?_ ?_
        · rw [hsplit]
          have : (slabFloor u : ℝ) ≤ (N : ℝ) := by exact_mod_cast hkN
          linarith
        · rw [hsplit]
          have : (N : ℝ) + 1 ≤ (slabCeil u : ℝ) := by exact_mod_cast hNK
          linarith
      have hone : bump y i (1 - y i) ∈ slabVertices u := by
        refine hchild (1 - y i) (Or.inr (by ring)) ?_ ?_
        · rw [hsplit]
          have : (slabFloor u : ℝ) ≤ (N : ℝ) := by exact_mod_cast hkN
          linarith
        · rw [hsplit]
          have : (N : ℝ) + 1 ≤ (slabCeil u : ℝ) := by exact_mod_cast hNK
          linarith
      have hcomb : (1 - y i) • bump y i (-y i) + y i • bump y i (1 - y i) = y := by
        funext l
        simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
        rcases eq_or_ne l i with rfl | hli
        · rw [bump_self, bump_self]; ring
        · rw [bump_of_ne _ _ _ hli, bump_of_ne _ _ _ hli]; ring
      rw [← hcomb]
      exact (convex_convexHull ℝ _) (subset_convexHull ℝ _ hzero) (subset_convexHull ℝ _ hone)
        (by linarith) (le_of_lt hilt) (by ring)
    · -- Two fractional coordinates: move them in opposite directions.
      obtain ⟨j, hj⟩ := not_forall.mp hsingle
      obtain ⟨hji, hjne⟩ := Classical.not_imp.mp hj
      have hj0 : y j ≠ 0 := fun h => hjne (Or.inl h)
      have hj1 : y j ≠ 1 := fun h => hjne (Or.inr h)
      have hjS : j ∈ s := by
        by_contra hns
        rcases hout j hns with h | h
        · exact hj0 h
        · exact hj1 h
      have hjc := hy.1 j
      have hjlt : 0 < y j := lt_of_le_of_ne hjc.1 (Ne.symm hj0)
      have hjut : y j < 1 := lt_of_le_of_ne hjc.2 hj1
      have hij : i ≠ j := Ne.symm hji
      have key : ∀ h : ℝ, 0 ≤ y i + h → y i + h ≤ 1 → 0 ≤ y j - h → y j - h ≤ 1 →
          (y i + h = 0 ∨ y i + h = 1 ∨ y j - h = 0 ∨ y j - h = 1) →
          bump (bump y i h) j (-h) ∈ convexHull ℝ (slabVertices u) := by
        intro h h1 h2 h3 h4 hint
        have hmem := bump_pair_mem_slab hy hij h h1 h2 h3 h4
        obtain ⟨c, hcs, hcint⟩ : ∃ c ∈ s,
            bump (bump y i h) j (-h) c = 0 ∨ bump (bump y i h) j (-h) c = 1 := by
          have hvi : bump (bump y i h) j (-h) i = y i + h := bump_pair_left y hij h
          have hvj : bump (bump y i h) j (-h) j = y j - h := bump_pair_right y hij h
          rcases hint with h' | h' | h' | h'
          · exact ⟨i, hiS, Or.inl (by rw [hvi]; exact h')⟩
          · exact ⟨i, hiS, Or.inr (by rw [hvi]; exact h')⟩
          · exact ⟨j, hjS, Or.inl (by rw [hvj]; exact h')⟩
          · exact ⟨j, hjS, Or.inr (by rw [hvj]; exact h')⟩
        refine IH _ (s.erase c) ?_ ?_ hmem
        · have hcard' := Finset.card_erase_of_mem hcs
          omega
        · intro l hl
          rcases eq_or_ne l c with rfl | hlc
          · exact hcint
          · have hls : l ∉ s := fun hx => hl (Finset.mem_erase.mpr ⟨hlc, hx⟩)
            have hli : l ≠ i := fun hx => hls (hx ▸ hiS)
            have hlj : l ≠ j := fun hx => hls (hx ▸ hjS)
            rw [bump_pair_other y i j h hli hlj]
            exact hout l hls
      have hamin := min_le_left (1 - y i) (y j)
      have hamin' := min_le_right (1 - y i) (y j)
      have hbmin := min_le_left (y i) (1 - y j)
      have hbmin' := min_le_right (y i) (1 - y j)
      have hapos : 0 < min (1 - y i) (y j) := lt_min (by linarith) hjlt
      have hbpos : 0 < min (y i) (1 - y j) := lt_min hilt (by linarith)
      have hplus := key (min (1 - y i) (y j)) (by linarith) (by linarith) (by linarith)
        (by linarith) (by
          rcases min_choice (1 - y i) (y j) with h | h
          · exact Or.inr (Or.inl (by rw [h]; ring))
          · exact Or.inr (Or.inr (Or.inl (by rw [h]; ring))))
      have hminus := key (-min (y i) (1 - y j)) (by linarith) (by linarith) (by linarith)
        (by linarith) (by
          rcases min_choice (y i) (1 - y j) with h | h
          · exact Or.inl (by rw [h]; ring)
          · exact Or.inr (Or.inr (Or.inr (by rw [h]; ring))))
      have hab : (0 : ℝ) < min (1 - y i) (y j) + min (y i) (1 - y j) := by linarith
      have habne : min (1 - y i) (y j) + min (y i) (1 - y j) ≠ 0 := ne_of_gt hab
      have hcomb :
          (min (y i) (1 - y j) / (min (1 - y i) (y j) + min (y i) (1 - y j))) •
              bump (bump y i (min (1 - y i) (y j))) j (-min (1 - y i) (y j)) +
            (min (1 - y i) (y j) / (min (1 - y i) (y j) + min (y i) (1 - y j))) •
              bump (bump y i (-min (y i) (1 - y j))) j (-(-min (y i) (1 - y j))) = y := by
        funext l
        simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
        rcases eq_or_ne l i with rfl | hli
        · rw [bump_pair_left y hij, bump_pair_left y hij]
          field_simp
          ring
        · rcases eq_or_ne l j with rfl | hlj
          · rw [bump_pair_right y hij, bump_pair_right y hij]
            field_simp
            ring
          · rw [bump_pair_other y i j _ hli hlj, bump_pair_other y i j _ hli hlj]
            field_simp
            ring
      rw [← hcomb]
      refine (convex_convexHull ℝ _) hplus hminus (by positivity) (by positivity) ?_
      field_simp
      ring

/-- **PB10, integrality.** Every point of the slab is a convex combination of
`0/1` points that themselves lie in the slab.  Degenerate cases are included:
the empty index type, an integral mean sum `S` (where the slab is a single
hyperplane slice of the cube), and an already integral `u`. -/
theorem slab_subset_convexHull_slabVertices (u : I → ℝ) :
    slab u ⊆ convexHull ℝ (slabVertices u) := fun y hy =>
  hull_aux u (Fintype.card I) y Finset.univ (le_of_eq Finset.card_univ)
    (fun l hl => absurd (Finset.mem_univ l) hl) hy

/-- Integrality in closed form: the slab is exactly the convex hull of its
integral points. -/
theorem convexHull_slabVertices_eq (u : I → ℝ) :
    convexHull ℝ (slabVertices u) = slab u :=
  Set.Subset.antisymm (convexHull_min (slabVertices_subset_slab u) (slab_convex u))
    (slab_subset_convexHull_slabVertices u)

/-- The equivalent extreme-point form of integrality: every extreme point of the
slab is a `0/1` point. -/
theorem extremePoints_slab_subset (u : I → ℝ) :
    (slab u).extremePoints ℝ ⊆ slabVertices u := by
  rw [← convexHull_slabVertices_eq u]
  exact extremePoints_convexHull_subset

/-! ## The adjacent-count law from integrality -/

section Laws

variable [DecidableEq I]

/-- **PB10, the consequence.** Integrality plus `u ∈ slab u` give a law with
means `u` supported on the integral points of the slab, that is, on the success
counts between `⌊S⌋` and `⌈S⌉`. -/
theorem exists_slabLaw {u : I → ℝ} (hu : u ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ u ∧
      ∀ v : Vertex I, μ.weight v ≠ 0 → slabFloor u ≤ count v ∧ count v ≤ slabCeil u := by
  classical
  have hmem : u ∈ convexHull ℝ (slabVertices u) :=
    slab_subset_convexHull_slabVertices u (mem_slab_self hu)
  have hrange : Set.range (fun w : {v : Vertex I // vertexPoint v ∈ slab u} =>
      vertexPoint w.val) = slabVertices u := by
    ext z
    constructor
    · rintro ⟨w, rfl⟩
      exact ⟨w.2, ⟨w.val, rfl⟩⟩
    · rintro ⟨hz, v, rfl⟩
      exact ⟨⟨v, hz⟩, rfl⟩
  rw [← hrange] at hmem
  obtain ⟨μ, hμ⟩ := (Law.mem_convexHull_range_iff _ u).mp hmem
  refine ⟨μ.map Subtype.val, fun i => ?_, fun v hv => ?_⟩
  · have h := congrFun hμ i
    simp only [Law.barycenter, Finset.sum_apply, Pi.smul_apply, smul_eq_mul] at h
    rw [Law.expect_map]
    simpa [Law.expect, Function.comp] using h
  · refine (vertexPoint_mem_slab_iff u v).mp ?_
    by_contra hns
    refine hv ?_
    simp only [Law.map]
    refine Finset.sum_eq_zero fun w _ => if_neg ?_
    rintro rfl
    exact hns w.2

/-- **PB10, re-derived.** The integrality route yields exactly the conclusion of
`exists_adjacentLaw` at the full support: a law with means `u` whose success
count is carried by the two adjacent integers `⌊S⌋` and `⌊S⌋ + 1`, with weights
`1 - (S - ⌊S⌋)` and `S - ⌊S⌋`.  When `S` is an integer the slab forces the count
to equal `⌊S⌋ = ⌈S⌉`, and the weight `S - ⌊S⌋` on the upper count is zero.

The direct construction `exists_adjacentLaw` is not used here and is not
replaced: it covers an arbitrary support `s`, whereas the slab of PB10 is the
full-dimensional one, `s = Finset.univ`. -/
theorem exists_adjacentLaw_of_slab {u : I → ℝ} (hu : u ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ u ∧ ∀ f : ℕ → ℝ,
      μ.expect (fun v => f (count v)) =
        (1 - countFrac Finset.univ u) * f (countFloor Finset.univ u) +
          countFrac Finset.univ u * f (countFloor Finset.univ u + 1) := by
  obtain ⟨μ, hmean, hsupp⟩ := exists_slabLaw hu
  refine ⟨μ, hmean, fun f => ?_⟩
  have hcount : μ.expect (fun v => (count v : ℝ)) = meanSum Finset.univ u := by
    simpa [countOn_univ] using expect_countOn Finset.univ u μ hmean
  have hpt : ∀ v : Vertex I, μ.weight v * f (count v) =
      μ.weight v * (f (countFloor Finset.univ u) +
        ((count v : ℝ) - (countFloor Finset.univ u : ℝ)) *
          (f (countFloor Finset.univ u + 1) - f (countFloor Finset.univ u))) := by
    intro v
    by_cases hw : μ.weight v = 0
    · simp [hw]
    · obtain ⟨h1, h2⟩ := hsupp v hw
      have h3 := slabCeil_le_slabFloor_add_one u
      have hcases : count v = slabFloor u ∨ count v = slabFloor u + 1 := by omega
      have hfl : slabFloor u = countFloor Finset.univ u := rfl
      rcases hcases with h | h <;> rw [h, hfl] <;> push_cast <;> ring
  have hexp : μ.expect (fun v => f (count v)) =
      μ.expect (fun v => f (countFloor Finset.univ u) +
        ((count v : ℝ) - (countFloor Finset.univ u : ℝ)) *
          (f (countFloor Finset.univ u + 1) - f (countFloor Finset.univ u))) := by
    simp only [Law.expect]
    exact Finset.sum_congr rfl fun v _ => hpt v
  rw [hexp]
  simp only [Law.expect_add, Law.expect_const, Law.expect_mul_const, Law.expect_sub]
  rw [hcount, countFrac]
  ring

end Laws

end

end MultilinearGap
