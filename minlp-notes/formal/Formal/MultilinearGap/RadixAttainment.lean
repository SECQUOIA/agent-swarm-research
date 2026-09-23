import Formal.MultilinearGap.RadixIncidence

/-!
# Exact attainment of the unit-box incidence bound (PB37)

`Formal/MultilinearGap/RadixIncidence.lean` proves the **upper** direction of PB37:
for the radix-`b` anchor/leaf family, every binary law with the prescribed marginals
of `Radix.means` satisfies `E ∑_j A_j N_j ≤ 1 + (L-1)/b`.  This file supplies the
matching **attaining law**, so that the source's equality

  `max E ∑_j A_j N_j = 1 + (L-1)/b`

becomes a theorem: `Radix.isGreatest_incidenceValues` and, in the source's regime
`b ≥ L`, `Radix.isGreatest_incidenceValues_of_le_radix`.

The construction follows `results/positive-multilinear-incidence-sharp-growth.md`:

* the nested anchor coupling, in which exactly the first `l` anchors are selected with
  probability `w_l = (b-1) b^-(l+1)` for `l < L` and `w_L = b^-L` (`levelWeight`, written
  here as the telescoping difference of the tail probabilities `tailWeight`);
* the two integer failure-count profiles `R = b ^ l` and `R = b ^ (l-1)`
  (`profileCount`), mixed with the weight `mixWeight b L` chosen so that `E R = 1`
  (`meanFailure_mixWeight`);
* a failed-leaf set realizing all block hit counts simultaneously, together with a
  uniform shift making every leaf marginal equal (`fiber`, `hitCount_fiber`).

Two points differ from the source's presentation, both simplifications:

* Every failure count occurring in the two profiles is a power `b ^ t`.  For such counts
  the source's "first `R` leaves in base-`b` digit-reversal order" can be replaced by the
  residue class `{i : i ≡ s (mod b ^ (L-t))}` (`fiber`), whose level-`j` hit count is
  `min (b ^ (j+1)) (b ^ t)` at every level at once (`hitCount_fiber`).  A uniform shift
  `s` over all leaves then gives each leaf failure probability `b ^ t / b ^ L`, so no
  digit-reversal ordering and no coordinatewise digit-shift group action is needed.
* The construction needs `0 ≤ mixWeight b L`, which holds exactly when `L ≤ b + 2`;
  the source's hypothesis `b ≥ L` is sufficient but not necessary.  The main theorem is
  therefore stated under `2 ≤ b`, `2 ≤ L` and `L ≤ b + 2`, with the `b ≥ L` corollary
  discharging PB37 as written.

The attainment is exactly the equality case of the dual certificate of `RadixIncidence`:
`objective_profileVertex` shows that at every vertex of the support the objective equals
`R + ∑_{k < l} dualWeight b k`, which is the pointwise dual bound with equality.
-/
namespace MultilinearGap
namespace Radix

noncomputable section
open scoped BigOperators

/-! ## Residue fibers as failed-leaf sets -/

/-- The set of leaves congruent to `s` modulo `b ^ (L - t)`; it has `b ^ t` elements
and hits exactly `min (b ^ (j+1)) (b ^ t)` blocks at every level `j`. -/
def fiber (b L t : ℕ) (s : Fin (b ^ L)) : Finset (Fin (b ^ L)) :=
  Finset.univ.filter (fun i => i.val % b ^ (L - t) = s.val % b ^ (L - t))

/-- Membership in a fiber is a congruence condition on the leaf index. -/
@[simp] theorem mem_fiber {b L t : ℕ} {s i : Fin (b ^ L)} :
    i ∈ fiber b L t s ↔ i.val % b ^ (L - t) = s.val % b ^ (L - t) := by
  simp [fiber]

/-- Two naturals in the same residue class modulo `u` with the same quotient by a
divisor `w` of `u` are equal. -/
theorem eq_of_mod_eq_of_div_eq {x y u w : ℕ} (hw : 0 < w) (hu : 0 < u) (hwu : w ∣ u)
    (hmod : x % u = y % u) (hdiv : x / w = y / w) : x = y := by
  rcases le_total x y with hxy | hxy
  · have hdvd : u ∣ y - x := (Nat.modEq_iff_dvd' hxy).mp hmod
    have hlt : y - x < w := by
      have h1 := Nat.div_add_mod x w
      have h2 := Nat.div_add_mod y w
      have h3 := Nat.mod_lt x hw
      have h4 := Nat.mod_lt y hw
      rw [hdiv] at h1
      omega
    have hwle : w ≤ u := Nat.le_of_dvd hu hwu
    have := Nat.eq_zero_of_dvd_of_lt hdvd (lt_of_lt_of_le hlt hwle)
    omega
  · have hdvd : u ∣ x - y := (Nat.modEq_iff_dvd' hxy).mp hmod.symm
    have hlt : x - y < w := by
      have h1 := Nat.div_add_mod x w
      have h2 := Nat.div_add_mod y w
      have h3 := Nat.mod_lt x hw
      have h4 := Nat.mod_lt y hw
      rw [hdiv] at h1
      omega
    have hwle : w ≤ u := Nat.le_of_dvd hu hwu
    have := Nat.eq_zero_of_dvd_of_lt hdvd (lt_of_lt_of_le hlt hwle)
    omega

/-- A fiber has exactly `b ^ t` leaves. -/
theorem fiber_card (b L t : ℕ) (hb : 1 ≤ b) (ht : t ≤ L) (s : Fin (b ^ L)) :
    (fiber b L t s).card = b ^ t := by
  have hb0 : 0 < b := hb
  have hu : 0 < b ^ (L - t) := pow_pos hb0 _
  have hsplit : b ^ L = b ^ t * b ^ (L - t) := by
    rw [← pow_add]; congr 1; omega
  have hsplit' : b ^ L = b ^ (L - t) * b ^ t := by rw [hsplit]; ring
  have hσ : s.val % b ^ (L - t) < b ^ (L - t) := Nat.mod_lt _ hu
  rw [← Finset.card_range (b ^ t)]
  refine Finset.card_bij (fun i _ => i.val / b ^ (L - t)) ?_ ?_ ?_
  · intro i _
    refine Finset.mem_range.mpr (Nat.div_lt_of_lt_mul ?_)
    exact lt_of_lt_of_le i.isLt (le_of_eq hsplit')
  · intro i hi j hj hij
    refine Fin.ext (eq_of_mod_eq_of_div_eq hu hu dvd_rfl ?_ hij)
    rw [mem_fiber] at hi hj
    rw [hi, hj]
  · intro k hk
    have hk' : k < b ^ t := Finset.mem_range.mp hk
    have hlt : k * b ^ (L - t) + s.val % b ^ (L - t) < b ^ L := by
      calc k * b ^ (L - t) + s.val % b ^ (L - t)
          < k * b ^ (L - t) + b ^ (L - t) := by omega
        _ = (k + 1) * b ^ (L - t) := by ring
        _ ≤ b ^ t * b ^ (L - t) := Nat.mul_le_mul_right _ hk'
        _ = b ^ L := hsplit.symm
    refine ⟨⟨k * b ^ (L - t) + s.val % b ^ (L - t), hlt⟩, ?_, ?_⟩
    · rw [mem_fiber]
      change (k * b ^ (L - t) + s.val % b ^ (L - t)) % b ^ (L - t) = s.val % b ^ (L - t)
      rw [Nat.add_comm, Nat.add_mul_mod_self_right, Nat.mod_mod_of_dvd _ dvd_rfl]
    · change (k * b ^ (L - t) + s.val % b ^ (L - t)) / b ^ (L - t) = k
      rw [Nat.add_comm, Nat.add_mul_div_right _ _ hu, Nat.div_eq_of_lt hσ, Nat.zero_add]

/-! ## Vertices with a prescribed anchor prefix and failed-leaf set -/

/-- The vertex selecting the first `l` anchors and failing exactly the leaves in `F`. -/
def boxVertex (b L l : ℕ) (F : Finset (Fin (b ^ L))) : CubicGap.Vertex (Coord b L) :=
  Sum.elim (fun j => decide (j.val < l)) (fun i => decide (i ∉ F))

/-- The failed leaves of `boxVertex` are exactly the prescribed set. -/
@[simp] theorem failedLeaves_boxVertex (b L l : ℕ) (F : Finset (Fin (b ^ L))) :
    failedLeaves b L (boxVertex b L l F) = F := by
  ext i
  simp [failedLeaves, boxVertex]

/-- The failure count of `boxVertex` is the size of the prescribed set. -/
@[simp] theorem failureCount_boxVertex (b L l : ℕ) (F : Finset (Fin (b ^ L))) :
    failureCount b L (boxVertex b L l F) = F.card := by
  simp [failureCount]

/-- `boxVertex` selects exactly the anchors of the first `l` levels. -/
@[simp] theorem vertexPoint_boxVertex_inl (b L l : ℕ) (F : Finset (Fin (b ^ L))) (j : Fin L) :
    CubicGap.vertexPoint (boxVertex b L l F) (Sum.inl j) = if j.val < l then 1 else 0 := by
  simp [CubicGap.vertexPoint, boxVertex]

/-- A leaf of `boxVertex` takes the value zero exactly when it fails. -/
@[simp] theorem vertexPoint_boxVertex_inr (b L l : ℕ) (F : Finset (Fin (b ^ L)))
    (i : Fin (b ^ L)) :
    CubicGap.vertexPoint (boxVertex b L l F) (Sum.inr i) = if i ∈ F then 0 else 1 := by
  by_cases h : i ∈ F <;> simp [CubicGap.vertexPoint, boxVertex, h]

/-- The blocks hit at `boxVertex` are the images of the failed leaves. -/
theorem hitBlocks_boxVertex (b L l : ℕ) (j : Fin L) (F : Finset (Fin (b ^ L))) :
    hitBlocks b L j (boxVertex b L l F) = F.image (fun i => (blockEquiv b L j i).1) := by
  rw [hitBlocks, failedLeaves_boxVertex]

/-! ## The block hit counts of a fiber -/

/-- A fiber at least as coarse as level `j` hits `b ^ t` distinct level-`j` blocks. -/
theorem hitCount_fiber_of_le (b L t l : ℕ) (hb : 1 ≤ b) (ht : t ≤ L) (j : Fin L)
    (hjt : t ≤ j.val + 1) (s : Fin (b ^ L)) :
    hitCount b L j (boxVertex b L l (fiber b L t s)) = b ^ t := by
  have hb0 : 0 < b := hb
  have hw : 0 < blockSize b L j := pow_pos hb0 _
  have hu : 0 < b ^ (L - t) := pow_pos hb0 _
  have hwu : blockSize b L j ∣ b ^ (L - t) := by
    rw [blockSize]
    exact pow_dvd_pow b (by omega)
  rw [hitCount, hitBlocks_boxVertex, Finset.card_image_of_injOn, fiber_card b L t hb ht s]
  intro i hi i' hi' hii
  rw [Finset.mem_coe, mem_fiber] at hi hi'
  refine Fin.ext (eq_of_mod_eq_of_div_eq hw hu hwu (by rw [hi, hi']) ?_)
  rw [← blockEquiv_fst_val, ← blockEquiv_fst_val]
  exact congrArg Fin.val hii

/-- A fiber finer than level `j` hits every level-`j` block. -/
theorem hitCount_fiber_of_ge (b L t l : ℕ) (hb : 1 ≤ b) (j : Fin L)
    (hjt : j.val + 1 ≤ t) (s : Fin (b ^ L)) :
    hitCount b L j (boxVertex b L l (fiber b L t s)) = b ^ (j.val + 1) := by
  have hb0 : 0 < b := hb
  have hw : 0 < blockSize b L j := pow_pos hb0 _
  have hu : 0 < b ^ (L - t) := pow_pos hb0 _
  have huw : b ^ (L - t) ∣ blockSize b L j := by
    rw [blockSize]
    exact pow_dvd_pow b (by omega)
  obtain ⟨d, hd⟩ := huw
  have hσ : s.val % b ^ (L - t) < b ^ (L - t) := Nat.mod_lt _ hu
  have hσw : s.val % b ^ (L - t) < blockSize b L j := by
    refine lt_of_lt_of_le hσ (Nat.le_of_dvd hw ⟨d, hd⟩)
  have himg : (fiber b L t s).image (fun i => (blockEquiv b L j i).1) = Finset.univ := by
    refine Finset.eq_univ_iff_forall.mpr fun c => Finset.mem_image.mpr ?_
    have hlt : c.val * blockSize b L j + s.val % b ^ (L - t) < b ^ L := by
      calc c.val * blockSize b L j + s.val % b ^ (L - t)
          < c.val * blockSize b L j + blockSize b L j := by omega
        _ = (c.val + 1) * blockSize b L j := by ring
        _ ≤ blockCount b L j * blockSize b L j := Nat.mul_le_mul_right _ c.isLt
        _ = b ^ L := blockCount_mul_blockSize b L j
    refine ⟨⟨c.val * blockSize b L j + s.val % b ^ (L - t), hlt⟩, ?_, ?_⟩
    · rw [mem_fiber]
      change (c.val * blockSize b L j + s.val % b ^ (L - t)) % b ^ (L - t)
        = s.val % b ^ (L - t)
      have hcw : c.val * blockSize b L j = c.val * d * b ^ (L - t) := by rw [hd]; ring
      rw [hcw, Nat.add_comm, Nat.add_mul_mod_self_right, Nat.mod_mod_of_dvd _ dvd_rfl]
    · refine Fin.ext ?_
      rw [blockEquiv_fst_val]
      change (c.val * blockSize b L j + s.val % b ^ (L - t)) / blockSize b L j = c.val
      rw [Nat.add_comm, Nat.add_mul_div_right _ _ hw, Nat.div_eq_of_lt hσw, Nat.zero_add]
  rw [hitCount, hitBlocks_boxVertex, himg, Finset.card_univ, Fintype.card_fin, blockCount]

/-- **Simultaneous realizability.**  A fiber of `b ^ t` leaves hits exactly
`min (b ^ (j+1)) (b ^ t)` blocks at *every* level `j` at once. -/
theorem hitCount_fiber (b L t l : ℕ) (hb : 1 ≤ b) (ht : t ≤ L) (j : Fin L) (s : Fin (b ^ L)) :
    hitCount b L j (boxVertex b L l (fiber b L t s)) = min (b ^ (j.val + 1)) (b ^ t) := by
  rcases le_total t (j.val + 1) with h | h
  · rw [hitCount_fiber_of_le b L t l hb ht j h s,
      min_eq_right (Nat.pow_le_pow_right hb h)]
  · rw [hitCount_fiber_of_ge b L t l hb j h s,
      min_eq_left (Nat.pow_le_pow_right hb h)]

/-- No block is hit when no leaf fails. -/
@[simp] theorem hitCount_empty (b L l : ℕ) (j : Fin L) :
    hitCount b L j (boxVertex b L l (∅ : Finset (Fin (b ^ L)))) = 0 := by
  simp [hitCount, hitBlocks_boxVertex]

/-! ## The two failure-count profiles -/

/-- The failed-leaf count of profile `p` at `l` selected anchors: `b ^ l` for the
first profile (`p = true`) and `b ^ (l-1)` for the second, each zero on the
initial levels where the source's profile vanishes. -/
def profileCount (b l : ℕ) (p : Bool) : ℕ :=
  if p then (if l = 0 then 0 else b ^ l) else (if l ≤ 1 then 0 else b ^ (l - 1))

/-- The failed-leaf set of profile `p` at `l` selected anchors and shift `s`. -/
def profileSet (b L l : ℕ) (p : Bool) (s : Fin (b ^ L)) : Finset (Fin (b ^ L)) :=
  if p then (if l = 0 then ∅ else fiber b L l s)
       else (if l ≤ 1 then ∅ else fiber b L (l - 1) s)

/-- The vertex of the attaining law at parameters `(l, p, s)`. -/
def profileVertex (b L l : ℕ) (p : Bool) (s : Fin (b ^ L)) : CubicGap.Vertex (Coord b L) :=
  boxVertex b L l (profileSet b L l p s)

/-- The profile set realizes the prescribed failure count. -/
theorem profileSet_card (b L l : ℕ) (hb : 1 ≤ b) (hl : l ≤ L) (p : Bool) (s : Fin (b ^ L)) :
    (profileSet b L l p s).card = profileCount b l p := by
  unfold profileSet profileCount
  cases p <;> simp only [if_true, if_false, Bool.false_eq_true] <;> split_ifs with h
  · simp
  · exact fiber_card b L (l - 1) hb (by omega) s
  · simp
  · exact fiber_card b L l hb hl s

/-- **Simultaneous realizability of the profile.**  At every level the profile set
hits exactly `min (b ^ (j+1)) R` blocks, the upper bound of the LP relaxation. -/
theorem hitCount_profileVertex (b L l : ℕ) (hb : 1 ≤ b) (hl : l ≤ L) (p : Bool)
    (s : Fin (b ^ L)) (j : Fin L) :
    hitCount b L j (profileVertex b L l p s) = min (b ^ (j.val + 1)) (profileCount b l p) := by
  unfold profileVertex profileSet profileCount
  cases p <;> simp only [if_true, if_false, Bool.false_eq_true] <;> split_ifs with h
  · simp
  · exact hitCount_fiber b L (l - 1) l hb (by omega) j s
  · simp
  · exact hitCount_fiber b L l l hb hl j s

/-! ## The pointwise objective at a profile vertex -/

/-- Truncating the level sum at `l ≤ L`. -/
theorem sum_fin_lt (L l : ℕ) (hl : l ≤ L) (f : ℕ → ℝ) :
    ∑ j : Fin L, (if j.val < l then (1 : ℝ) else 0) * f j.val = ∑ k ∈ Finset.range l, f k := by
  have hfilter : Finset.filter (fun k => k < l) (Finset.range L) = Finset.range l := by
    ext k
    simp only [Finset.mem_filter, Finset.mem_range]
    omega
  rw [Fin.sum_univ_eq_sum_range (fun k => (if k < l then (1 : ℝ) else 0) * f k) L]
  rw [Finset.sum_congr rfl (fun k _ => by split_ifs <;> simp :
      ∀ k ∈ Finset.range L, (if k < l then (1 : ℝ) else 0) * f k = if k < l then f k else 0),
    ← Finset.sum_filter, hfilter]

/-- The geometric identity behind the equality case: `∑_{k<l} b^(k+1) = b^l + ∑_{k<l} w_k`
for `l ≥ 1`, where `w` is the dual weight of `RadixIncidence`. -/
theorem sum_pow_succ_eq (b n : ℕ) :
    ∑ k ∈ Finset.range (n + 1), (b : ℝ) ^ (k + 1)
      = (b : ℝ) ^ (n + 1) + ∑ k ∈ Finset.range (n + 1), dualWeight b k := by
  induction n with
  | zero => simp [dualWeight]
  | succ n ih =>
    rw [Finset.sum_range_succ (fun k => (b : ℝ) ^ (k + 1)), ih,
      Finset.sum_range_succ (fun k => dualWeight b k) (n + 1)]
    have : dualWeight b (n + 1) = (b : ℝ) ^ (n + 1) := by simp [dualWeight]
    rw [this]
    ring

/-- **The equality case of the dual certificate.**  At a profile vertex the objective
equals the dual bound `R + ∑_{k<l} w_k` exactly, for both profiles and every `l`. -/
theorem objective_profileVertex (b L l : ℕ) (hb : 1 ≤ b) (hl : l ≤ L) (p : Bool)
    (s : Fin (b ^ L)) :
    (∑ j, CubicGap.vertexPoint (profileVertex b L l p s) (Sum.inl j)
        * (hitCount b L j (profileVertex b L l p s) : ℝ))
      = (profileCount b l p : ℝ) + ∑ k ∈ Finset.range l, dualWeight b k := by
  have hb1 : (1 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb
  have hstep : ∀ j : Fin L, CubicGap.vertexPoint (profileVertex b L l p s) (Sum.inl j)
      * (hitCount b L j (profileVertex b L l p s) : ℝ)
      = (if j.val < l then (1 : ℝ) else 0)
          * ((min (b ^ (j.val + 1)) (profileCount b l p) : ℕ) : ℝ) := by
    intro j
    rw [hitCount_profileVertex b L l hb hl p s j]
    simp [profileVertex]
  rw [Finset.sum_congr rfl (fun j _ => hstep j),
    sum_fin_lt L l hl (fun k => ((min (b ^ (k + 1)) (profileCount b l p) : ℕ) : ℝ))]
  -- now a pure computation with the two profiles
  cases p
  · -- second profile: `R = b ^ (l-1)`
    rcases Nat.lt_or_ge l 2 with hl2 | hl2
    · interval_cases l <;> simp [profileCount, dualWeight]
    · obtain ⟨n, rfl⟩ : ∃ n, l = n + 2 := ⟨l - 2, by omega⟩
      have hR : profileCount b (n + 2) false = b ^ (n + 1) := by
        simp [profileCount]
      rw [hR]
      have hterm : ∀ k ∈ Finset.range (n + 1),
          ((min (b ^ (k + 1)) (b ^ (n + 1)) : ℕ) : ℝ) = (b : ℝ) ^ (k + 1) := by
        intro k hk
        have : k + 1 ≤ n + 1 := by simpa using Nat.succ_le_of_lt (Finset.mem_range.mp hk)
        rw [min_eq_left (Nat.pow_le_pow_right hb this)]
        push_cast
        ring
      rw [Finset.sum_range_succ (fun k => ((min (b ^ (k + 1)) (b ^ (n + 1)) : ℕ) : ℝ)) (n + 1),
        Finset.sum_congr rfl hterm,
        min_eq_right (Nat.pow_le_pow_right hb (by omega : n + 1 ≤ n + 2)),
        sum_pow_succ_eq b n,
        Finset.sum_range_succ (fun k => dualWeight b k) (n + 1)]
      have hdw : dualWeight b (n + 1) = (b : ℝ) ^ (n + 1) := by simp [dualWeight]
      rw [hdw]
      push_cast
      ring
  · -- first profile: `R = b ^ l`
    rcases Nat.eq_zero_or_pos l with rfl | hl1
    · simp [profileCount]
    · obtain ⟨n, rfl⟩ : ∃ n, l = n + 1 := ⟨l - 1, by omega⟩
      have hR : profileCount b (n + 1) true = b ^ (n + 1) := by simp [profileCount]
      rw [hR]
      have hterm : ∀ k ∈ Finset.range (n + 1),
          ((min (b ^ (k + 1)) (b ^ (n + 1)) : ℕ) : ℝ) = (b : ℝ) ^ (k + 1) := by
        intro k hk
        have : k + 1 ≤ n + 1 := by simpa using Nat.succ_le_of_lt (Finset.mem_range.mp hk)
        rw [min_eq_left (Nat.pow_le_pow_right hb this)]
        push_cast
        ring
      rw [Finset.sum_congr rfl hterm, sum_pow_succ_eq b n]
      push_cast
      ring

/-! ## The nested anchor coupling -/

/-- The probability that at least the first `k` anchors are selected, namely `b ^ -k`,
truncated to zero above the top level. -/
def tailWeight (b L k : ℕ) : ℝ := if k ≤ L then 1 / (b : ℝ) ^ k else 0

/-- The probability that exactly the first `l` anchors are selected:
`(b-1) b ^ -(l+1)` below the top level and `b ^ -L` at it. -/
def levelWeight (b L l : ℕ) : ℝ := tailWeight b L l - tailWeight b L (l + 1)

/-- The level weights are nonnegative. -/
theorem levelWeight_nonneg (b L l : ℕ) (hb : 1 ≤ b) : 0 ≤ levelWeight b L l := by
  have hb1 : (1 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb
  have hpos : (0 : ℝ) < (b : ℝ) ^ l := by positivity
  unfold levelWeight tailWeight
  by_cases h1 : l + 1 ≤ L
  · have h2 : l ≤ L := by omega
    rw [if_pos h1, if_pos h2]
    have : (b : ℝ) ^ l ≤ (b : ℝ) ^ (l + 1) := pow_le_pow_right₀ hb1 (Nat.le_succ l)
    have := one_div_le_one_div_of_le hpos this
    linarith
  · rw [if_neg h1]
    by_cases h2 : l ≤ L
    · rw [if_pos h2]
      have : (0 : ℝ) < 1 / (b : ℝ) ^ l := by positivity
      linarith
    · rw [if_neg h2]
      norm_num

/-- The level weights telescope. -/
theorem sum_levelWeight_range (b L n : ℕ) :
    ∑ l ∈ Finset.range n, levelWeight b L l = tailWeight b L 0 - tailWeight b L n :=
  Finset.sum_range_sub' (fun k => tailWeight b L k) n

/-- The nested coupling is a probability distribution on `{0, …, L}`. -/
theorem sum_levelWeight (b L : ℕ) : ∑ l ∈ Finset.range (L + 1), levelWeight b L l = 1 := by
  rw [sum_levelWeight_range]
  simp [tailWeight]

/-- The upper tail of the nested coupling gives the prescribed anchor mean. -/
theorem sum_levelWeight_Ico (b L a : ℕ) (ha : a ≤ L + 1) :
    ∑ l ∈ Finset.Ico a (L + 1), levelWeight b L l = tailWeight b L a := by
  rw [Finset.sum_Ico_eq_sub _ ha, sum_levelWeight_range, sum_levelWeight_range]
  have : tailWeight b L (L + 1) = 0 := by simp [tailWeight]
  rw [this]
  ring

/-! ## The attaining law -/

/-- The index set of the attaining law: the number of selected anchors, the profile,
and the shift selecting the failed-leaf fiber. -/
abbrev AttIndex (b L : ℕ) := Fin (L + 1) × Bool × Fin (b ^ L)

/-- The nested anchor coupling, as a law on the number of selected anchors. -/
def levelLaw (b L : ℕ) (hb : 1 ≤ b) : CubicGap.Law (Fin (L + 1)) where
  weight l := levelWeight b L l.val
  nonneg l := levelWeight_nonneg b L l.val hb
  mass_one := by
    rw [Fin.sum_univ_eq_sum_range (fun k => levelWeight b L k) (L + 1)]
    exact sum_levelWeight b L

/-- The mixture of the two failure-count profiles, with weight `θ` on the first. -/
def profileLaw (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ 1) : CubicGap.Law Bool where
  weight p := if p then θ else 1 - θ
  nonneg p := by cases p <;> simpa using by linarith
  mass_one := by rw [Fintype.sum_bool]; norm_num

/-- The uniform shift, as a law on the leaves. -/
def shiftLaw (b L : ℕ) (hb : 1 ≤ b) : CubicGap.Law (Fin (b ^ L)) where
  weight _ := 1 / (b : ℝ) ^ L
  nonneg _ := by
    have : (0 : ℝ) < (b : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hb
    positivity
  mass_one := by
    have hb0 : (0 : ℝ) < (b : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hb
    have hpow : ((b : ℝ) ^ L) ≠ 0 := by positivity
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    push_cast
    field_simp

/-- The law on the index set: the nested anchor coupling, the profile mixture, and an
independent uniform shift, all independent. -/
def attIndexLaw (b L : ℕ) (hb : 1 ≤ b) (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ 1) :
    CubicGap.Law (AttIndex b L) :=
  (levelLaw b L hb).prod ((profileLaw θ h0 h1).prod (shiftLaw b L hb))

/-- Expectations under the index law: average over the shift, mix the two profiles,
then average over the nested coupling. -/
theorem attIndexLaw_expect (b L : ℕ) (hb : 1 ≤ b) (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ 1)
    (G : ℕ → Bool → Fin (b ^ L) → ℝ) :
    (attIndexLaw b L hb θ h0 h1).expect (fun x => G x.1.val x.2.1 x.2.2)
      = ∑ l ∈ Finset.range (L + 1), levelWeight b L l *
          (θ * ((∑ s, G l true s) / (b : ℝ) ^ L)
            + (1 - θ) * ((∑ s, G l false s) / (b : ℝ) ^ L)) := by
  have hfin : (attIndexLaw b L hb θ h0 h1).expect (fun x => G x.1.val x.2.1 x.2.2)
      = ∑ l : Fin (L + 1), (fun k => levelWeight b L k *
          (θ * ((∑ s, G k true s) / (b : ℝ) ^ L)
            + (1 - θ) * ((∑ s, G k false s) / (b : ℝ) ^ L))) l.val := by
    rw [attIndexLaw]
    simp only [CubicGap.Law.expect_prod]
    simp only [CubicGap.Law.expect, Fintype.sum_bool, levelLaw, profileLaw, shiftLaw,
      if_true, if_false, Bool.false_eq_true]
    refine Finset.sum_congr rfl fun l _ => ?_
    rw [← Finset.mul_sum, ← Finset.mul_sum]
    ring
  rw [hfin]
  exact Fin.sum_univ_eq_sum_range (fun k => levelWeight b L k *
    (θ * ((∑ s, G k true s) / (b : ℝ) ^ L)
      + (1 - θ) * ((∑ s, G k false s) / (b : ℝ) ^ L))) (L + 1)

/-- Expectations of quantities that do not depend on the shift. -/
theorem attIndexLaw_expect_of_const (b L : ℕ) (hb : 1 ≤ b) (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ 1)
    (G : ℕ → Bool → ℝ) :
    (attIndexLaw b L hb θ h0 h1).expect (fun x => G x.1.val x.2.1)
      = ∑ l ∈ Finset.range (L + 1), levelWeight b L l * (θ * G l true + (1 - θ) * G l false) := by
  have hb0 : (0 : ℝ) < (b : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hb
  have hcard : ((b ^ L : ℕ) : ℝ) = (b : ℝ) ^ L := by push_cast; ring
  have hpow : ((b : ℝ) ^ L) ≠ 0 := by positivity
  rw [attIndexLaw_expect b L hb θ h0 h1 (fun l p _ => G l p)]
  refine Finset.sum_congr rfl fun l _ => ?_
  rw [Finset.sum_const, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    nsmul_eq_mul, hcard]
  field_simp

/-! ## The three moments of the nested coupling -/

/-- The mean failure count of the first profile, `((L-1)(b-1) + b)/b` of the source. -/
theorem sum_levelWeight_profileCount_true (b L : ℕ) (hb : 1 ≤ b) (hL : 1 ≤ L) :
    ∑ l ∈ Finset.range (L + 1), levelWeight b L l * (profileCount b l true : ℝ)
      = ((L : ℝ) - 1) * (1 - 1 / b) + 1 := by
  have hb0 : (0 : ℝ) < (b : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hb
  obtain ⟨M, rfl⟩ : ∃ M, L = M + 1 := ⟨L - 1, by omega⟩
  have hg0 : levelWeight b (M + 1) 0 * (profileCount b 0 true : ℝ) = 0 := by
    simp [profileCount]
  have hgi : ∀ i ∈ Finset.range M,
      levelWeight b (M + 1) (i + 1) * (profileCount b (i + 1) true : ℝ) = 1 - 1 / b := by
    intro i hi
    have hi' := Finset.mem_range.mp hi
    simp only [levelWeight, tailWeight, profileCount, if_pos (by omega : i + 1 ≤ M + 1),
      if_pos (by omega : i + 1 + 1 ≤ M + 1), if_neg (by omega : ¬ i + 1 = 0), if_true]
    push_cast
    field_simp
    ring
  have hgtop : levelWeight b (M + 1) (M + 1) * (profileCount b (M + 1) true : ℝ) = 1 := by
    simp only [levelWeight, tailWeight, profileCount, if_pos (le_refl (M + 1)),
      if_neg (by omega : ¬ M + 1 + 1 ≤ M + 1), if_neg (by omega : ¬ M + 1 = 0), if_true]
    push_cast
    field_simp
    ring
  rw [Finset.sum_range_succ (fun l => levelWeight b (M + 1) l * (profileCount b l true : ℝ))
      (M + 1),
    Finset.sum_range_succ' (fun l => levelWeight b (M + 1) l * (profileCount b l true : ℝ)) M,
    hg0, hgtop, Finset.sum_congr rfl hgi, Finset.sum_const, Finset.card_range, nsmul_eq_mul]
  push_cast
  ring

/-- The mean failure count of the second profile, `((L-2)(b-1) + b)/b²` of the source. -/
theorem sum_levelWeight_profileCount_false (b L : ℕ) (hb : 1 ≤ b) (hL : 2 ≤ L) :
    ∑ l ∈ Finset.range (L + 1), levelWeight b L l * (profileCount b l false : ℝ)
      = ((L : ℝ) - 2) * (1 - 1 / b) / b + 1 / b := by
  have hb0 : (0 : ℝ) < (b : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hb
  obtain ⟨M, rfl⟩ : ∃ M, L = M + 2 := ⟨L - 2, by omega⟩
  have hg0 : levelWeight b (M + 2) 0 * (profileCount b 0 false : ℝ) = 0 := by
    simp [profileCount]
  have hg1 : levelWeight b (M + 2) 1 * (profileCount b 1 false : ℝ) = 0 := by
    simp [profileCount]
  have hgi : ∀ i ∈ Finset.range M,
      levelWeight b (M + 2) (i + 1 + 1) * (profileCount b (i + 1 + 1) false : ℝ)
        = (1 - 1 / b) / b := by
    intro i hi
    have hi' := Finset.mem_range.mp hi
    simp only [levelWeight, tailWeight, profileCount, if_pos (by omega : i + 1 + 1 ≤ M + 2),
      if_pos (by omega : i + 1 + 1 + 1 ≤ M + 2), if_neg (by omega : ¬ i + 1 + 1 ≤ 1),
      Bool.false_eq_true, if_false]
    have : i + 1 + 1 - 1 = i + 1 := by omega
    rw [this]
    push_cast
    field_simp
    ring
  have hgtop : levelWeight b (M + 2) (M + 2) * (profileCount b (M + 2) false : ℝ) = 1 / b := by
    simp only [levelWeight, tailWeight, profileCount, if_pos (le_refl (M + 2)),
      if_neg (by omega : ¬ M + 2 + 1 ≤ M + 2), if_neg (by omega : ¬ M + 2 ≤ 1),
      Bool.false_eq_true, if_false]
    have : M + 2 - 1 = M + 1 := by omega
    rw [this]
    push_cast
    field_simp
    ring
  rw [Finset.sum_range_succ (fun l => levelWeight b (M + 2) l * (profileCount b l false : ℝ))
      (M + 2),
    Finset.sum_range_succ' (fun l => levelWeight b (M + 2) l * (profileCount b l false : ℝ))
      (M + 1),
    Finset.sum_range_succ' (fun l => levelWeight b (M + 2) (l + 1)
      * (profileCount b (l + 1) false : ℝ)) M,
    hg0, hg1, hgtop, Finset.sum_congr rfl hgi, Finset.sum_const, Finset.card_range, nsmul_eq_mul]
  push_cast
  field_simp
  ring

/-- The dual weights average to `(L-1)/b` under the nested coupling: this is the dual
objective value of `RadixIncidence`. -/
theorem sum_levelWeight_dual (b L : ℕ) (hb : 1 ≤ b) (hL : 1 ≤ L) :
    ∑ l ∈ Finset.range (L + 1), levelWeight b L l * (∑ k ∈ Finset.range l, dualWeight b k)
      = ((L : ℝ) - 1) / b := by
  have hexch : ∑ l ∈ Finset.range (L + 1), ∑ k ∈ Finset.range l,
        levelWeight b L l * dualWeight b k
      = ∑ k ∈ Finset.range (L + 1), ∑ l ∈ Finset.Ico (k + 1) (L + 1),
        levelWeight b L l * dualWeight b k :=
    Finset.sum_comm' (by
      intro x y
      simp only [Finset.mem_range, Finset.mem_Ico]
      omega)
  have hinner : ∀ k ∈ Finset.range (L + 1),
      ∑ l ∈ Finset.Ico (k + 1) (L + 1), levelWeight b L l * dualWeight b k
        = tailWeight b L (k + 1) * dualWeight b k := by
    intro k hk
    have hk' := Finset.mem_range.mp hk
    rw [← Finset.sum_mul, sum_levelWeight_Ico b L (k + 1) (by omega)]
  have hterm : ∀ k ∈ Finset.range L,
      tailWeight b L (k + 1) * dualWeight b k = dualWeight b k * (1 / (b : ℝ) ^ (k + 1)) := by
    intro k hk
    have hk' := Finset.mem_range.mp hk
    rw [tailWeight, if_pos (by omega : k + 1 ≤ L)]
    ring
  simp only [Finset.mul_sum]
  rw [hexch, Finset.sum_congr rfl hinner,
    Finset.sum_range_succ (fun k => tailWeight b L (k + 1) * dualWeight b k) L,
    Finset.sum_congr rfl hterm]
  have htop : tailWeight b L (L + 1) = 0 := by simp [tailWeight]
  rw [htop, zero_mul, add_zero]
  exact sum_range_dualWeight b hb L hL

/-! ## The mixture and its mean failure count -/

/-- The mean failure count of the profile mixture with weight `θ`. -/
def meanFailure (b L : ℕ) (θ : ℝ) : ℝ :=
  θ * (((L : ℝ) - 1) * (1 - 1 / b) + 1) + (1 - θ) * (((L : ℝ) - 2) * (1 - 1 / b) / b + 1 / b)

/-- The mean failure count of the mixture, in closed form. -/
theorem sum_levelWeight_mix (b L : ℕ) (hb : 1 ≤ b) (hL : 2 ≤ L) (θ : ℝ) :
    ∑ l ∈ Finset.range (L + 1), levelWeight b L l
        * (θ * (profileCount b l true : ℝ) + (1 - θ) * (profileCount b l false : ℝ))
      = meanFailure b L θ := by
  have hstep : ∀ l ∈ Finset.range (L + 1), levelWeight b L l
      * (θ * (profileCount b l true : ℝ) + (1 - θ) * (profileCount b l false : ℝ))
      = θ * (levelWeight b L l * (profileCount b l true : ℝ))
        + (1 - θ) * (levelWeight b L l * (profileCount b l false : ℝ)) := by
    intro l _
    ring
  rw [Finset.sum_congr rfl hstep, Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum,
    sum_levelWeight_profileCount_true b L hb (by omega),
    sum_levelWeight_profileCount_false b L hb hL]
  rfl

/-- The mixing weight making the mean failure count one. -/
def mixWeight (b L : ℕ) : ℝ := ((b : ℝ) - L + 2) / ((L : ℝ) * ((b : ℝ) - 1) + 2)

/-- The mixing weight is nonnegative exactly in the regime `L ≤ b + 2`, which is
where this hypothesis (weaker than the source's `b ≥ L`) is used. -/
theorem mixWeight_nonneg (b L : ℕ) (hb : 2 ≤ b) (hL : 2 ≤ L) (hbL : L ≤ b + 2) :
    0 ≤ mixWeight b L := by
  have hb1 : (2 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb
  have hL1 : (2 : ℝ) ≤ (L : ℝ) := by exact_mod_cast hL
  have hbL1 : (L : ℝ) ≤ (b : ℝ) + 2 := by exact_mod_cast hbL
  have hden : (0 : ℝ) < (L : ℝ) * ((b : ℝ) - 1) + 2 := by nlinarith
  exact div_nonneg (by linarith) (le_of_lt hden)

/-- The mixing weight is at most one. -/
theorem mixWeight_le_one (b L : ℕ) (hb : 2 ≤ b) (hL : 2 ≤ L) : mixWeight b L ≤ 1 := by
  have hb1 : (2 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb
  have hL1 : (2 : ℝ) ≤ (L : ℝ) := by exact_mod_cast hL
  have hden : (0 : ℝ) < (L : ℝ) * ((b : ℝ) - 1) + 2 := by nlinarith
  rw [mixWeight, div_le_one hden]
  nlinarith

/-- **The mean-one mixture.**  With weight `mixWeight b L` the mixture has mean failure
count exactly one, which is the prescribed leaf marginal constraint. -/
theorem meanFailure_mixWeight (b L : ℕ) (hb : 2 ≤ b) (hL : 2 ≤ L) :
    meanFailure b L (mixWeight b L) = 1 := by
  have hb0 : (0 : ℝ) < (b : ℝ) := by
    have : (2 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb
    linarith
  have hb1 : (2 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb
  have hL1 : (2 : ℝ) ≤ (L : ℝ) := by exact_mod_cast hL
  have hden : ((L : ℝ) * ((b : ℝ) - 1) + 2) ≠ 0 := by nlinarith
  unfold meanFailure mixWeight
  field_simp
  ring

/-! ## The attaining law and its marginals -/

/-- **The attaining law.**  The nested anchor coupling, the two failure-count profiles
mixed with weight `θ`, and a uniform shift of the failed-leaf fiber, pushed forward to
the vertices of the cube. -/
def attLaw (b L : ℕ) (hb : 1 ≤ b) (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ 1) :
    CubicGap.Law (CubicGap.Vertex (Coord b L)) :=
  (attIndexLaw b L hb θ h0 h1).map (fun x => profileVertex b L x.1.val x.2.1 x.2.2)

/-- The anchor marginals of the attaining law are the prescribed `b ^ -(j+1)`. -/
theorem attLaw_expect_anchor (b L : ℕ) (hb : 1 ≤ b) (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ 1)
    (j : Fin L) :
    (attLaw b L hb θ h0 h1).expect (fun v => CubicGap.vertexPoint v (Sum.inl j))
      = means b L (Sum.inl j) := by
  have hfun : ((fun v => CubicGap.vertexPoint v (Sum.inl j)) ∘
      fun x : AttIndex b L => profileVertex b L x.1.val x.2.1 x.2.2)
      = fun x : AttIndex b L => (fun (l : ℕ) (_ : Bool) => if j.val < l then (1 : ℝ) else 0)
        x.1.val x.2.1 := by
    funext x
    simp [profileVertex]
  have hset : Finset.filter (fun l => j.val < l) (Finset.range (L + 1))
      = Finset.Ico (j.val + 1) (L + 1) := by
    ext l
    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_Ico]
    omega
  have hsummand : ∀ l ∈ Finset.range (L + 1), levelWeight b L l
      * (θ * (if j.val < l then (1 : ℝ) else 0) + (1 - θ) * (if j.val < l then (1 : ℝ) else 0))
      = if j.val < l then levelWeight b L l else 0 := by
    intro l _
    split_ifs <;> ring
  rw [attLaw, CubicGap.Law.expect_map, hfun,
    attIndexLaw_expect_of_const b L hb θ h0 h1
      (fun (l : ℕ) (_ : Bool) => if j.val < l then (1 : ℝ) else 0),
    Finset.sum_congr rfl hsummand, ← Finset.sum_filter, hset,
    sum_levelWeight_Ico b L (j.val + 1) (by omega),
    tailWeight, if_pos (by omega : j.val + 1 ≤ L), means, blockCount]
  push_cast
  ring

/-- The number of shifts placing a given leaf in the failed set is the failure count. -/
theorem filter_mem_profileSet_card (b L l : ℕ) (hb : 1 ≤ b) (hl : l ≤ L) (p : Bool)
    (i : Fin (b ^ L)) :
    (Finset.univ.filter (fun s => i ∈ profileSet b L l p s)).card = profileCount b l p := by
  have hfib : ∀ t : ℕ, t ≤ L →
      (Finset.univ.filter (fun s => i ∈ fiber b L t s)).card = b ^ t := by
    intro t ht
    have : Finset.univ.filter (fun s => i ∈ fiber b L t s) = fiber b L t i := by
      ext s
      simp only [Finset.mem_filter, Finset.mem_univ, true_and, mem_fiber]
      exact eq_comm
    rw [this, fiber_card b L t hb ht i]
  unfold profileSet profileCount
  cases p <;> simp only [if_true, if_false, Bool.false_eq_true] <;> split_ifs with h
  · simp
  · exact hfib (l - 1) (by omega)
  · simp
  · exact hfib l hl

/-- The shift average of the leaf indicator: each leaf fails with probability `R / b ^ L`. -/
theorem sum_shift_leaf (b L l : ℕ) (hb : 1 ≤ b) (hl : l ≤ L) (p : Bool) (i : Fin (b ^ L)) :
    ∑ s : Fin (b ^ L), (if i ∈ profileSet b L l p s then (0 : ℝ) else 1)
      = (b : ℝ) ^ L - (profileCount b l p : ℝ) := by
  have hcard : ((b ^ L : ℕ) : ℝ) = (b : ℝ) ^ L := by push_cast; ring
  have h1 : ∀ s : Fin (b ^ L), (if i ∈ profileSet b L l p s then (0 : ℝ) else 1)
      = 1 - (if i ∈ profileSet b L l p s then (1 : ℝ) else 0) := by
    intro s
    split_ifs <;> ring
  rw [Finset.sum_congr rfl (fun s _ => h1 s), Finset.sum_sub_distrib, Finset.sum_const,
    Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one, hcard, Finset.sum_boole,
    filter_mem_profileSet_card b L l hb hl p i]

/-- The leaf marginals of the attaining law: each leaf fails with probability
`meanFailure / b ^ L`. -/
theorem attLaw_expect_leaf (b L : ℕ) (hb : 1 ≤ b) (hL : 2 ≤ L) (θ : ℝ) (h0 : 0 ≤ θ)
    (h1 : θ ≤ 1) (i : Fin (b ^ L)) :
    (attLaw b L hb θ h0 h1).expect (fun v => CubicGap.vertexPoint v (Sum.inr i))
      = 1 - meanFailure b L θ / (b : ℝ) ^ L := by
  have hb0 : (0 : ℝ) < (b : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hb
  have hpow : ((b : ℝ) ^ L) ≠ 0 := by positivity
  have hfun : ((fun v => CubicGap.vertexPoint v (Sum.inr i)) ∘
      fun x : AttIndex b L => profileVertex b L x.1.val x.2.1 x.2.2)
      = fun x : AttIndex b L =>
        (fun (l : ℕ) (p : Bool) (s : Fin (b ^ L)) =>
          if i ∈ profileSet b L l p s then (0 : ℝ) else 1) x.1.val x.2.1 x.2.2 := by
    funext x
    simp [profileVertex]
  have hstep : ∀ l ∈ Finset.range (L + 1), levelWeight b L l
      * (θ * ((∑ s, if i ∈ profileSet b L l true s then (0 : ℝ) else 1) / (b : ℝ) ^ L)
        + (1 - θ) * ((∑ s, if i ∈ profileSet b L l false s then (0 : ℝ) else 1) / (b : ℝ) ^ L))
      = levelWeight b L l
        - levelWeight b L l * (θ * (profileCount b l true : ℝ)
            + (1 - θ) * (profileCount b l false : ℝ)) / (b : ℝ) ^ L := by
    intro l hl
    have hl' : l ≤ L := by
      have := Finset.mem_range.mp hl
      omega
    rw [sum_shift_leaf b L l hb hl' true i, sum_shift_leaf b L l hb hl' false i]
    field_simp
    ring
  rw [attLaw, CubicGap.Law.expect_map, hfun,
    attIndexLaw_expect b L hb θ h0 h1
      (fun (l : ℕ) (p : Bool) (s : Fin (b ^ L)) =>
        if i ∈ profileSet b L l p s then (0 : ℝ) else 1),
    Finset.sum_congr rfl hstep, Finset.sum_sub_distrib, sum_levelWeight b L, ← Finset.sum_div,
    sum_levelWeight_mix b L hb hL θ]

/-- The objective of the attaining law: the dual bound with the mean failure count. -/
theorem attLaw_expect_objective (b L : ℕ) (hb : 1 ≤ b) (hL : 2 ≤ L) (θ : ℝ) (h0 : 0 ≤ θ)
    (h1 : θ ≤ 1) :
    (attLaw b L hb θ h0 h1).expect
        (fun v => ∑ j, CubicGap.vertexPoint v (Sum.inl j) * (hitCount b L j v : ℝ))
      = meanFailure b L θ + ((L : ℝ) - 1) / b := by
  have hfun : ((fun v => ∑ j, CubicGap.vertexPoint v (Sum.inl j) * (hitCount b L j v : ℝ)) ∘
      fun x : AttIndex b L => profileVertex b L x.1.val x.2.1 x.2.2)
      = fun x : AttIndex b L =>
        (fun (l : ℕ) (p : Bool) => (profileCount b l p : ℝ)
          + ∑ k ∈ Finset.range l, dualWeight b k) x.1.val x.2.1 := by
    funext x
    exact objective_profileVertex b L x.1.val hb (Nat.lt_succ_iff.mp x.1.isLt) x.2.1 x.2.2
  have hstep : ∀ l ∈ Finset.range (L + 1), levelWeight b L l
      * (θ * ((profileCount b l true : ℝ) + ∑ k ∈ Finset.range l, dualWeight b k)
        + (1 - θ) * ((profileCount b l false : ℝ) + ∑ k ∈ Finset.range l, dualWeight b k))
      = levelWeight b L l * (θ * (profileCount b l true : ℝ)
          + (1 - θ) * (profileCount b l false : ℝ))
        + levelWeight b L l * (∑ k ∈ Finset.range l, dualWeight b k) := by
    intro l _
    ring
  rw [attLaw, CubicGap.Law.expect_map, hfun,
    attIndexLaw_expect_of_const b L hb θ h0 h1
      (fun (l : ℕ) (p : Bool) => (profileCount b l p : ℝ)
        + ∑ k ∈ Finset.range l, dualWeight b k),
    Finset.sum_congr rfl hstep, Finset.sum_add_distrib, sum_levelWeight_mix b L hb hL θ,
    sum_levelWeight_dual b L hb (by omega)]

/-! ## PB37: the exact value of the unit-box incidence maximum -/

/-- The objective values `E ∑_j A_j N_j` attainable by binary laws with the anchor and
leaf marginals prescribed by `Radix.means`. -/
def incidenceValues (b L : ℕ) : Set ℝ :=
  {x | ∃ μ : CubicGap.Law (CubicGap.Vertex (Coord b L)),
    (∀ j : Fin L,
      μ.expect (fun v => CubicGap.vertexPoint v (Sum.inl j)) = means b L (Sum.inl j)) ∧
    (∀ i : Fin (b ^ L),
      μ.expect (fun v => CubicGap.vertexPoint v (Sum.inr i)) = means b L (Sum.inr i)) ∧
    μ.expect (fun v => ∑ j, CubicGap.vertexPoint v (Sum.inl j) * (hitCount b L j v : ℝ)) = x}

/-- **PB37, lower direction.**  The bound `1 + (L-1)/b` is attained by the explicit
law `attLaw` with mixing weight `mixWeight b L`. -/
theorem incidence_attained (b L : ℕ) (hb : 2 ≤ b) (hL : 2 ≤ L) (hbL : L ≤ b + 2) :
    (1 + ((L : ℝ) - 1) / b) ∈ incidenceValues b L := by
  refine ⟨attLaw b L (by omega) (mixWeight b L) (mixWeight_nonneg b L hb hL hbL)
    (mixWeight_le_one b L hb hL), fun j => ?_, fun i => ?_, ?_⟩
  · exact attLaw_expect_anchor b L (by omega) (mixWeight b L) _ _ j
  · rw [attLaw_expect_leaf b L (by omega) hL (mixWeight b L) _ _ i,
      meanFailure_mixWeight b L hb hL]
    simp [means]
  · rw [attLaw_expect_objective b L (by omega) hL (mixWeight b L) _ _,
      meanFailure_mixWeight b L hb hL]

/-- **PB37.**  For `2 ≤ b` and `2 ≤ L ≤ b + 2` the maximum of `E ∑_j A_j N_j` over the
binary laws with the prescribed marginals is exactly `1 + (L-1)/b`: the upper bound of
`RadixIncidence` and the attaining law of this file. -/
theorem isGreatest_incidenceValues (b L : ℕ) (hb : 2 ≤ b) (hL : 2 ≤ L) (hbL : L ≤ b + 2) :
    IsGreatest (incidenceValues b L) (1 + ((L : ℝ) - 1) / b) := by
  refine ⟨incidence_attained b L hb hL hbL, ?_⟩
  rintro x ⟨μ, hanchor, hleaf, rfl⟩
  exact incidence_expect_le_of_means b L (by omega) (by omega) μ hanchor hleaf

/-- **PB37 as an exact supremum.** -/
theorem sSup_incidenceValues (b L : ℕ) (hb : 2 ≤ b) (hL : 2 ≤ L) (hbL : L ≤ b + 2) :
    sSup (incidenceValues b L) = 1 + ((L : ℝ) - 1) / b :=
  (isGreatest_incidenceValues b L hb hL hbL).csSup_eq

/-- **PB37 in the source's regime `b ≥ L`.**  This is the statement imported by
`results/positive-multilinear-positive-box-lower.md`:
`max E ∑_j A_j N_j = 1 + (L-1)/b` for `b ≥ L`. -/
theorem isGreatest_incidenceValues_of_le_radix (b L : ℕ) (hL : 2 ≤ L) (hbL : L ≤ b) :
    IsGreatest (incidenceValues b L) (1 + ((L : ℝ) - 1) / b) :=
  isGreatest_incidenceValues b L (by omega) hL (by omega)

end
end Radix
end MultilinearGap
