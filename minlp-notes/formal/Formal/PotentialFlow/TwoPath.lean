import Formal.PotentialFlow.Optimization

/-!
# The two-path certified example

For every path length `L ≥ 1` this module builds the network of `ex:a-cert-paths`:
two internally disjoint source-sink paths, each of length `L`, every edge oriented
toward the sink, all positive and negative coefficients equal to one, source
nomination `2`, sink nomination `-2` and zero internal nominations.

## Encoding

The network `net L : Network (2 * L) (2 * L)` has `2 * L` nodes and `2 * L` edges.

* Node `0` is the source and node `1` is the sink.  For `1 ≤ i ≤ L - 1` the `i`-th
  internal node of path `p ∈ {0, 1}` is node `2 + p * (L - 1) + (i - 1)`; this is
  `nodeIdx L p i`, which also returns `0` for `i = 0` and `1` for `i = L`.
* Edge `k` lies on path `k / L` at position `k % L`; its tail is the node at
  position `k % L` of that path and its head the node at position `k % L + 1`.
  Equivalently, the edge at position `i < L` of path `p < 2` has index `p * L + i`.
* `pathFlow L s t` is the flow with value `s` on every edge of path `0` and `t` on
  every edge of path `1`; `pathFlow L 1 1` is the constant-one flow and
  `pathFlow L (1 + eps) (1 - eps)` is the trial flow of the example.
* `potential L` is the integral potential `L - i` at the node at position `i` of
  either path, so the source has potential `L` and the sink potential `0`.

## Main results

* `feasible_iff`: the conserved flows are exactly the `pathFlow L t (2 - t)`.
* `potential_terminals`, `sum_drops_path`: the source and sink potentials `L` and `0`, and
  the resulting path drop `L` on each of the two paths.
* `one_minimizer`, `exists_unique_physical`, `exists_unique_minimizer`,
  `eq_pathFlow_one_of_physical`, `eq_pathFlow_one_of_minimizer`: the constant-one
  flow is the unique physical flow and the unique energy minimizer.
* `familyEnergy_eq`, `familyEnergy_strictConvexOn`, `familyEnergy_symm`,
  `familyEnergy_lt_of_le_of_lt`: the energy along the conserved family.
* `gap_eq`, `dualLower_eq`, `certified_gap_eq`: the exact gap `2 * L * eps ^ 2`
  and the matching dual value `2 * L / 3`.

All statements are proved for a general `L`, with `0 < L` assumed wherever it is
needed; the degenerate case `L = 1` (two parallel edges, no internal node) is
included.
-/

namespace PotentialFlow.TwoPath

noncomputable section

/-! ### Index bookkeeping -/

/-- Node index of the node at position `i` on path `p`: position `0` is the source,
position `L` is the sink, and `1 ≤ i ≤ L - 1` gives an internal node of path `p`. -/
def nodeIdx (L p i : ℕ) : ℕ :=
  if i = 0 then 0 else if i = L then 1 else 2 + p * (L - 1) + (i - 1)

/-- Every node index of a path of length `L` is a legitimate node of the network. -/
theorem nodeIdx_lt {L p i : ℕ} (hL : 0 < L) (hp : p < 2) (hi : i ≤ L) :
    nodeIdx L p i < 2 * L := by
  unfold nodeIdx
  split
  · omega
  · split
    · omega
    · interval_cases p <;> omega

/-- The source is the only node at position `0`. -/
theorem nodeIdx_eq_zero {L p i : ℕ} (hL : 0 < L) (hp : p < 2) (_hi : i ≤ L) :
    nodeIdx L p i = 0 ↔ i = 0 := by
  unfold nodeIdx
  by_cases h0 : i = 0
  · rw [if_pos h0]; omega
  · rw [if_neg h0]
    by_cases h1 : i = L
    · rw [if_pos h1]; omega
    · rw [if_neg h1]; interval_cases p <;> omega

/-- The sink is the only node at position `L`. -/
theorem nodeIdx_eq_one {L p i : ℕ} (hL : 0 < L) (hp : p < 2) (_hi : i ≤ L) :
    nodeIdx L p i = 1 ↔ i = L := by
  unfold nodeIdx
  by_cases h0 : i = 0
  · rw [if_pos h0]; omega
  · rw [if_neg h0]
    by_cases h1 : i = L
    · rw [if_pos h1]; omega
    · rw [if_neg h1]; interval_cases p <;> omega

/-- Internal nodes determine both the path and the position. -/
theorem nodeIdx_eq_internal {L p i p' i' : ℕ} (hL : 0 < L) (hp : p < 2) (hi : i ≤ L)
    (hp' : p' < 2) (hi1 : 1 ≤ i') (hi2 : i' < L) :
    nodeIdx L p i = 2 + p' * (L - 1) + (i' - 1) ↔ (p = p' ∧ i = i') := by
  unfold nodeIdx
  by_cases h0 : i = 0
  · rw [if_pos h0]; interval_cases p' <;> omega
  · rw [if_neg h0]
    by_cases h1 : i = L
    · rw [if_pos h1]; interval_cases p' <;> omega
    · rw [if_neg h1]; interval_cases p <;> interval_cases p' <;> omega

/-- The edge at position `i < L` of path `p` has index `p * L + i`. -/
theorem edgeIdx_div {L p i : ℕ} (hL : 0 < L) (hi : i < L) : (p * L + i) / L = p := by
  rw [mul_comm, Nat.mul_add_div hL, Nat.div_eq_of_lt hi, Nat.add_zero]

/-- The position of the edge with index `p * L + i` is `i`. -/
theorem edgeIdx_mod {L p i : ℕ} (hi : i < L) : (p * L + i) % L = i := by
  rw [add_comm, Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hi]

/-- A network with `2 * L` nodes is nonempty only when the paths are nonempty. -/
theorem len_pos {L : ℕ} (v : Fin (2 * L)) : 0 < L := by
  have := v.isLt; omega

/-- Every edge lies on path `0` or path `1`. -/
theorem pathNum_lt {L : ℕ} (e : Fin (2 * L)) : (e : ℕ) / L < 2 :=
  Nat.div_lt_of_lt_mul (by have := e.isLt; omega)

/-- Every edge sits at a position strictly below `L`. -/
theorem posNum_lt {L : ℕ} (e : Fin (2 * L)) : (e : ℕ) % L < L :=
  Nat.mod_lt _ (len_pos e)

/-! ### The network, its nominations, flows and potentials -/

/-- The two-path network: `2 * L` nodes, `2 * L` edges, all coefficients one. -/
def net (L : ℕ) : Network (2 * L) (2 * L) where
  tail e := ⟨nodeIdx L ((e : ℕ) / L) ((e : ℕ) % L),
    nodeIdx_lt (len_pos e) (pathNum_lt e) (posNum_lt e).le⟩
  head e := ⟨nodeIdx L ((e : ℕ) / L) ((e : ℕ) % L + 1),
    nodeIdx_lt (len_pos e) (pathNum_lt e) (posNum_lt e)⟩
  positive _ := 1
  negative _ := 1

@[simp] theorem tail_val (L : ℕ) (e : Fin (2 * L)) :
    ((net L).tail e : ℕ) = nodeIdx L ((e : ℕ) / L) ((e : ℕ) % L) := rfl

@[simp] theorem head_val (L : ℕ) (e : Fin (2 * L)) :
    ((net L).head e : ℕ) = nodeIdx L ((e : ℕ) / L) ((e : ℕ) % L + 1) := rfl

@[simp] theorem positive_apply (L : ℕ) (e : Fin (2 * L)) : (net L).positive e = 1 := rfl

@[simp] theorem negative_apply (L : ℕ) (e : Fin (2 * L)) : (net L).negative e = 1 := rfl

/-- Tails are compared through node indices. -/
theorem tail_eq_iff {L : ℕ} (e v : Fin (2 * L)) :
    (net L).tail e = v ↔ nodeIdx L ((e : ℕ) / L) ((e : ℕ) % L) = (v : ℕ) := by
  rw [Fin.ext_iff, tail_val]

/-- Heads are compared through node indices. -/
theorem head_eq_iff {L : ℕ} (e v : Fin (2 * L)) :
    (net L).head e = v ↔ nodeIdx L ((e : ℕ) / L) ((e : ℕ) % L + 1) = (v : ℕ) := by
  rw [Fin.ext_iff, head_val]

/-- Nominations: `2` at the source, `-2` at the sink and `0` at every internal node. -/
def nom (L : ℕ) : Fin (2 * L) → ℝ := fun v =>
  if (v : ℕ) = 0 then 2 else if (v : ℕ) = 1 then -2 else 0

/-- The flow with value `s` on every edge of path `0` and `t` on every edge of path `1`. -/
def pathFlow (L : ℕ) (s t : ℝ) : Fin (2 * L) → ℝ := fun e => if (e : ℕ) < L then s else t

theorem pathFlow_apply (L : ℕ) (s t : ℝ) (e : Fin (2 * L)) :
    pathFlow L s t e = if (e : ℕ) < L then s else t := rfl

/-- The flow value on an edge of path `0`. -/
theorem pathFlow_first {L : ℕ} (s t : ℝ) (a : Fin (2 * L)) (ha : (a : ℕ) < L) :
    pathFlow L s t a = s := if_pos ha

/-- The flow value on an edge of path `1`. -/
theorem pathFlow_second {L : ℕ} (s t : ℝ) (a : Fin (2 * L)) (ha : L ≤ (a : ℕ)) :
    pathFlow L s t a = t := if_neg (by omega)

/-- The constant-one flow. -/
theorem pathFlow_one_apply (L : ℕ) (e : Fin (2 * L)) : pathFlow L 1 1 e = 1 := by
  rw [pathFlow_apply]; split <;> rfl

/-- Integral potentials: `L - i` at the node at position `i` of either path. -/
def potential (L : ℕ) : Fin (2 * L) → ℝ := fun v =>
  if (v : ℕ) = 0 then (L : ℝ)
  else if (v : ℕ) = 1 then 0
  else (L : ℝ) - 1 - (((v : ℕ) - 2) % (L - 1) : ℕ)

/-- Unfolding lemma for the integral potentials. -/
theorem potential_apply (L : ℕ) (v : Fin (2 * L)) :
    potential L v =
      if (v : ℕ) = 0 then (L : ℝ)
      else if (v : ℕ) = 1 then 0
      else (L : ℝ) - 1 - (((v : ℕ) - 2) % (L - 1) : ℕ) := rfl

/-- The potential at the node at position `i` of any path is `L - i`. -/
theorem potential_of_val {L p i : ℕ} (hL : 0 < L) (_hp : p < 2) (hi : i ≤ L)
    (v : Fin (2 * L)) (hv : (v : ℕ) = nodeIdx L p i) :
    potential L v = (L : ℝ) - i := by
  by_cases h0 : i = 0
  · have hn : nodeIdx L p i = 0 := by unfold nodeIdx; rw [if_pos h0]
    rw [potential_apply, hv, hn, if_pos rfl, h0]
    norm_num
  · by_cases h1 : i = L
    · have hn : nodeIdx L p i = 1 := by unfold nodeIdx; rw [if_neg h0, if_pos h1]
      rw [potential_apply, hv, hn, if_neg one_ne_zero, if_pos rfl, h1]
      norm_num
    · have hi1 : 1 ≤ i := by omega
      have hL2 : 2 ≤ L := by omega
      have hn : nodeIdx L p i = 2 + p * (L - 1) + (i - 1) := by
        unfold nodeIdx; rw [if_neg h0, if_neg h1]
      rw [potential_apply, hv, hn,
        if_neg (by omega : ¬(2 + p * (L - 1) + (i - 1) = 0)),
        if_neg (by omega : ¬(2 + p * (L - 1) + (i - 1) = 1)),
        show 2 + p * (L - 1) + (i - 1) - 2 = (L - 1) * p + (i - 1) by
          rw [Nat.mul_comm]; omega,
        Nat.mul_add_mod, Nat.mod_eq_of_lt (by omega), Nat.cast_sub hi1]
      push_cast
      ring

/-- The potential at the tail of an edge is `L` minus the edge's position. -/
theorem potential_tail (L : ℕ) (e : Fin (2 * L)) :
    potential L ((net L).tail e) = (L : ℝ) - ((e : ℕ) % L : ℕ) :=
  potential_of_val (len_pos e) (pathNum_lt e) (posNum_lt e).le _ (tail_val L e)

/-- The potential at the head of an edge is one less than at its tail. -/
theorem potential_head (L : ℕ) (e : Fin (2 * L)) :
    potential L ((net L).head e) = (L : ℝ) - ((e : ℕ) % L : ℕ) - 1 := by
  rw [potential_of_val (len_pos e) (pathNum_lt e) (posNum_lt e) _ (head_val L e)]
  push_cast
  ring

/-- Every edge has potential drop exactly one. -/
theorem drops_potential (L : ℕ) (e : Fin (2 * L)) : (net L).drops (potential L) e = 1 := by
  rw [Network.drops, potential_tail, potential_head]
  ring

/-- The source carries the integral potential `L` and the sink the potential `0`. -/
theorem potential_terminals {L : ℕ} (hL : 0 < L) :
    potential L ⟨0, by omega⟩ = (L : ℝ) ∧ potential L ⟨1, by omega⟩ = 0 := by
  have hsrc : ((⟨0, by omega⟩ : Fin (2 * L)) : ℕ) = nodeIdx L 0 0 := by
    unfold nodeIdx; rw [if_pos rfl]
  have hsnk : ((⟨1, by omega⟩ : Fin (2 * L)) : ℕ) = nodeIdx L 0 L := by
    unfold nodeIdx; rw [if_neg (by omega : ¬(L = 0)), if_pos rfl]
  constructor
  · rw [potential_of_val hL (by norm_num : (0 : ℕ) < 2) (Nat.zero_le L) _ hsrc]
    norm_num
  · rw [potential_of_val hL (by norm_num : (0 : ℕ) < 2) (le_refl L) _ hsnk]
    ring

/-- **CC31.**  The potential drop along either path of the example is exactly `L`: the path
has `L` edges, each of unit drop, so the drops telescope from the source potential `L` to
the sink potential `0`. -/
theorem sum_drops_path {L p : ℕ} (hp : p < 2) :
    ∑ i : Fin L, (net L).drops (potential L)
        ⟨p * L + (i : ℕ), by
          have hi := i.isLt
          rcases (show p = 0 ∨ p = 1 by omega) with rfl | rfl <;> omega⟩ = (L : ℝ) := by
  rw [Finset.sum_congr rfl (fun i _ => drops_potential L _), Finset.sum_const,
    Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one]

/-! ### Conservation -/

private theorem sum_eq_pair {N : ℕ} (f : Fin N → ℝ) (a b : Fin N) (hab : a ≠ b)
    (h : ∀ c, c ≠ a → c ≠ b → f c = 0) : ∑ c, f c = f a + f b := by
  classical
  rw [← Finset.sum_subset (Finset.subset_univ ({a, b} : Finset (Fin N)))
    (fun c _ hc => h c (fun hca => hc (by simp [hca])) (fun hcb => hc (by simp [hcb])))]
  exact Finset.sum_pair hab

/-- Only the first edges of the two paths leave the source. -/
theorem loads_source {L : ℕ} (x : Fin (2 * L) → ℝ) (v a b : Fin (2 * L))
    (hv : (v : ℕ) = 0) (ha : (a : ℕ) = 0) (hb : (b : ℕ) = L) :
    (net L).loads x v = x a + x b := by
  have hL : 0 < L := len_pos v
  have htail : ∀ c : Fin (2 * L), (net L).tail c = v ↔ (c : ℕ) % L = 0 := by
    intro c
    rw [tail_eq_iff, hv]
    exact nodeIdx_eq_zero hL (pathNum_lt c) (posNum_lt c).le
  have hhead : ∀ c : Fin (2 * L), ¬((net L).head c = v) := by
    intro c
    rw [head_eq_iff, hv, nodeIdx_eq_zero hL (pathNum_lt c) (posNum_lt c)]
    omega
  have hab : a ≠ b := by intro h; rw [h] at ha; omega
  have hzero : ∀ c : Fin (2 * L), c ≠ a → c ≠ b → (net L).incidence v c * x c = 0 := by
    intro c hca hcb
    have hc0 : ¬((c : ℕ) % L = 0) := by
      intro hc0
      obtain ⟨q, hq⟩ : ∃ q, (c : ℕ) / L = q := ⟨_, rfl⟩
      have hd : L * q + (c : ℕ) % L = (c : ℕ) := by rw [← hq]; exact Nat.div_add_mod _ _
      have h2 : q < 2 := by rw [← hq]; exact pathNum_lt c
      interval_cases q
      · exact hca (Fin.ext (by omega))
      · exact hcb (Fin.ext (by omega))
    simp only [Network.incidence, if_neg (fun h => hc0 ((htail c).mp h)), if_neg (hhead c),
      sub_zero, zero_mul]
  have hva : (net L).incidence v a * x a = x a := by
    simp only [Network.incidence, if_pos ((htail a).mpr (by rw [ha]; exact Nat.zero_mod L)),
      if_neg (hhead a), sub_zero, one_mul]
  have hvb : (net L).incidence v b * x b = x b := by
    simp only [Network.incidence, if_pos ((htail b).mpr (by rw [hb]; exact Nat.mod_self L)),
      if_neg (hhead b), sub_zero, one_mul]
  rw [Network.loads_apply, sum_eq_pair _ a b hab hzero, hva, hvb]

/-- Only the last edges of the two paths enter the sink. -/
theorem loads_sink {L : ℕ} (x : Fin (2 * L) → ℝ) (v a b : Fin (2 * L))
    (hv : (v : ℕ) = 1) (ha : (a : ℕ) = L - 1) (hb : (b : ℕ) = 2 * L - 1) :
    (net L).loads x v = -(x a + x b) := by
  have hL : 0 < L := len_pos v
  have htail : ∀ c : Fin (2 * L), ¬((net L).tail c = v) := by
    intro c
    rw [tail_eq_iff, hv, nodeIdx_eq_one hL (pathNum_lt c) (posNum_lt c).le]
    have := posNum_lt c
    omega
  have hhead : ∀ c : Fin (2 * L), (net L).head c = v ↔ (c : ℕ) % L = L - 1 := by
    intro c
    rw [head_eq_iff, hv, nodeIdx_eq_one hL (pathNum_lt c) (posNum_lt c)]
    have := posNum_lt c
    omega
  have hab : a ≠ b := by intro h; rw [h] at ha; omega
  have hA : (a : ℕ) % L = L - 1 := by rw [ha, Nat.mod_eq_of_lt (by omega)]
  have hB : (b : ℕ) % L = L - 1 := by
    rw [hb, show 2 * L - 1 = L + (L - 1) by omega, Nat.add_mod_left,
      Nat.mod_eq_of_lt (by omega)]
  have hzero : ∀ c : Fin (2 * L), c ≠ a → c ≠ b → (net L).incidence v c * x c = 0 := by
    intro c hca hcb
    have hc0 : ¬((c : ℕ) % L = L - 1) := by
      intro hc0
      obtain ⟨q, hq⟩ : ∃ q, (c : ℕ) / L = q := ⟨_, rfl⟩
      have hd : L * q + (c : ℕ) % L = (c : ℕ) := by rw [← hq]; exact Nat.div_add_mod _ _
      have h2 : q < 2 := by rw [← hq]; exact pathNum_lt c
      interval_cases q
      · exact hca (Fin.ext (by omega))
      · exact hcb (Fin.ext (by omega))
    simp only [Network.incidence, if_neg (htail c), if_neg (fun h => hc0 ((hhead c).mp h)),
      sub_zero, zero_mul]
  have hva : (net L).incidence v a * x a = -x a := by
    simp only [Network.incidence, if_neg (htail a), if_pos ((hhead a).mpr hA), zero_sub,
      neg_one_mul]
  have hvb : (net L).incidence v b * x b = -x b := by
    simp only [Network.incidence, if_neg (htail b), if_pos ((hhead b).mpr hB), zero_sub,
      neg_one_mul]
  rw [Network.loads_apply, sum_eq_pair _ a b hab hzero, hva, hvb]
  ring

private theorem edge_val_eq_iff {L p i : ℕ} (hL : 0 < L) (hi : i < L) (c d : Fin (2 * L))
    (hd : (d : ℕ) = p * L + i) :
    ((c : ℕ) / L = p ∧ (c : ℕ) % L = i) ↔ c = d := by
  constructor
  · rintro ⟨h1, h2⟩
    refine Fin.ext ?_
    have hdm := Nat.div_add_mod (c : ℕ) L
    rw [h1, h2] at hdm
    rw [hd, ← hdm, mul_comm]
  · rintro rfl
    rw [hd]
    exact ⟨edgeIdx_div hL hi, edgeIdx_mod hi⟩

/-- An internal node is met by exactly the two consecutive edges of its own path. -/
theorem loads_internal {L p i : ℕ} (hp : p < 2) (hi1 : 1 ≤ i) (hi2 : i < L)
    (x : Fin (2 * L) → ℝ) (v a b : Fin (2 * L))
    (hv : (v : ℕ) = 2 + p * (L - 1) + (i - 1))
    (ha : (a : ℕ) = p * L + i) (hb : (b : ℕ) = p * L + (i - 1)) :
    (net L).loads x v = x a - x b := by
  have hL : 0 < L := len_pos v
  have htail : ∀ c : Fin (2 * L), (net L).tail c = v ↔ c = a := by
    intro c
    rw [tail_eq_iff, hv,
      nodeIdx_eq_internal hL (pathNum_lt c) (posNum_lt c).le hp hi1 hi2]
    exact edge_val_eq_iff hL hi2 c a ha
  have hhead : ∀ c : Fin (2 * L), (net L).head c = v ↔ c = b := by
    intro c
    rw [head_eq_iff, hv,
      nodeIdx_eq_internal hL (pathNum_lt c) (posNum_lt c) hp hi1 hi2,
      show ((c : ℕ) % L + 1 = i) ↔ ((c : ℕ) % L = i - 1) from by omega]
    exact edge_val_eq_iff hL (by omega) c b hb
  have hab : a ≠ b := by intro h; rw [h] at ha; omega
  have hzero : ∀ c : Fin (2 * L), c ≠ a → c ≠ b → (net L).incidence v c * x c = 0 := by
    intro c hca hcb
    simp only [Network.incidence, if_neg (fun h => hca ((htail c).mp h)),
      if_neg (fun h => hcb ((hhead c).mp h)), sub_zero, zero_mul]
  have hva : (net L).incidence v a * x a = x a := by
    simp only [Network.incidence, if_pos ((htail a).mpr rfl),
      if_neg (fun h => hab ((hhead a).mp h)), sub_zero, one_mul]
  have hvb : (net L).incidence v b * x b = -x b := by
    simp only [Network.incidence, if_neg (fun h => hab.symm ((htail b).mp h)),
      if_pos ((hhead b).mpr rfl), zero_sub, neg_one_mul]
  rw [Network.loads_apply, sum_eq_pair _ a b hab hzero, hva, hvb]
  ring

/-- Every node other than the two terminals is an internal node of a unique path. -/
theorem exists_internal {L : ℕ} (v : Fin (2 * L)) (hv : 2 ≤ (v : ℕ)) :
    ∃ p i : ℕ, p < 2 ∧ 1 ≤ i ∧ i < L ∧ (v : ℕ) = 2 + p * (L - 1) + (i - 1) := by
  have hLt := v.isLt
  have hpos : 0 < L - 1 := by omega
  obtain ⟨p, i, hp, hi, hval⟩ :
      ∃ p i : ℕ, p < 2 ∧ i < L - 1 ∧ (v : ℕ) - 2 = p * (L - 1) + i := by
    exact ⟨((v : ℕ) - 2) / (L - 1), ((v : ℕ) - 2) % (L - 1),
      Nat.div_lt_of_lt_mul (by omega), Nat.mod_lt _ hpos, (Nat.div_add_mod' _ _).symm⟩
  exact ⟨p, i + 1, hp, by omega, by omega, by omega⟩

/-- Every path-constant flow with values summing to two is conserved. -/
theorem feasible_pathFlow {L : ℕ} (hL : 0 < L) (t : ℝ) :
    (net L).Feasible (nom L) (pathFlow L t (2 - t)) := by
  funext v
  rcases Nat.lt_or_ge (v : ℕ) 2 with hv | hv
  · rcases (show (v : ℕ) = 0 ∨ (v : ℕ) = 1 by omega) with hval | hval
    · have ha : ((⟨0, by omega⟩ : Fin (2 * L)) : ℕ) = 0 := rfl
      have hb : ((⟨L, by omega⟩ : Fin (2 * L)) : ℕ) = L := rfl
      rw [loads_source (pathFlow L t (2 - t)) v ⟨0, by omega⟩ ⟨L, by omega⟩ hval ha hb,
        pathFlow_first t (2 - t) _ (by rw [ha]; exact hL),
        pathFlow_second t (2 - t) _ hb.ge]
      simp only [nom, if_pos hval]
      ring
    · have ha : ((⟨L - 1, by omega⟩ : Fin (2 * L)) : ℕ) = L - 1 := rfl
      have hb : ((⟨2 * L - 1, by omega⟩ : Fin (2 * L)) : ℕ) = 2 * L - 1 := rfl
      rw [loads_sink (pathFlow L t (2 - t)) v ⟨L - 1, by omega⟩ ⟨2 * L - 1, by omega⟩
          hval ha hb,
        pathFlow_first t (2 - t) _ (by rw [ha]; omega),
        pathFlow_second t (2 - t) _ (by rw [hb]; omega)]
      simp only [nom, if_neg (by omega : ¬((v : ℕ) = 0)), if_pos hval]
      ring
  · obtain ⟨p, i, hp, hi1, hi2, hval⟩ := exists_internal v hv
    have hba : p * L + i < 2 * L := by interval_cases p <;> omega
    have hbb : p * L + (i - 1) < 2 * L := by interval_cases p <;> omega
    rw [loads_internal hp hi1 hi2 (pathFlow L t (2 - t)) v ⟨p * L + i, hba⟩
      ⟨p * L + (i - 1), hbb⟩ hval rfl rfl]
    simp only [nom, if_neg (by omega : ¬((v : ℕ) = 0)), if_neg (by omega : ¬((v : ℕ) = 1))]
    rcases (show p = 0 ∨ p = 1 by omega) with rfl | rfl
    · rw [pathFlow_first t (2 - t) _ (show 0 * L + i < L by omega),
        pathFlow_first t (2 - t) _ (show 0 * L + (i - 1) < L by omega)]
      ring
    · rw [pathFlow_second t (2 - t) _ (show L ≤ 1 * L + i by omega),
        pathFlow_second t (2 - t) _ (show L ≤ 1 * L + (i - 1) by omega)]
      ring

/-- Conservation at the internal nodes forces each path's flow to be constant. -/
theorem flow_eq_base {L : ℕ} {x : Fin (2 * L) → ℝ} (hfeas : (net L).Feasible (nom L) x)
    (p : ℕ) (hp : p < 2) :
    ∀ (i : ℕ), i < L → ∀ a b : Fin (2 * L), (a : ℕ) = p * L + i → (b : ℕ) = p * L → x a = x b := by
  intro i
  induction i with
  | zero => intro _ a b ha hb; exact congrArg x (Fin.ext (by omega))
  | succ k ih =>
    intro hk a b ha hb
    have haLt := a.isLt
    have hcb : p * L + k < 2 * L := by omega
    have hvb : 2 + p * (L - 1) + k < 2 * L := by interval_cases p <;> omega
    have hstep := loads_internal (L := L) (p := p) (i := k + 1) hp (by omega) hk x
      ⟨2 + p * (L - 1) + k, hvb⟩ a ⟨p * L + k, hcb⟩
      (show 2 + p * (L - 1) + k = 2 + p * (L - 1) + (k + 1 - 1) by omega) ha
      (show p * L + k = p * L + (k + 1 - 1) by omega)
    have hnomv : nom L ⟨2 + p * (L - 1) + k, hvb⟩ = 0 := by
      simp only [nom]
      rw [if_neg (show ¬(2 + p * (L - 1) + k = 0) by omega),
        if_neg (show ¬(2 + p * (L - 1) + k = 1) by omega)]
    have hz : x a - x ⟨p * L + k, hcb⟩ = 0 := by
      rw [← hstep, congrFun hfeas, hnomv]
    have := ih (by omega) ⟨p * L + k, hcb⟩ b rfl hb
    linarith [hz, this]

/-- The conserved flows are exactly the path-constant flows with values summing to two. -/
theorem feasible_iff {L : ℕ} (hL : 0 < L) (x : Fin (2 * L) → ℝ) :
    (net L).Feasible (nom L) x ↔ ∃ t : ℝ, x = pathFlow L t (2 - t) := by
  constructor
  · intro hfeas
    have hsrc := loads_source x ⟨0, by omega⟩ ⟨0, by omega⟩ ⟨L, by omega⟩ rfl rfl rfl
    have hnomv : nom L (⟨0, by omega⟩ : Fin (2 * L)) = 2 := by simp [nom]
    have hsum : x (⟨0, by omega⟩ : Fin (2 * L)) + x (⟨L, by omega⟩ : Fin (2 * L)) = 2 := by
      rw [← hsrc, congrFun hfeas, hnomv]
    refine ⟨x ⟨0, by omega⟩, ?_⟩
    funext e
    obtain ⟨q, hq⟩ : ∃ q, (e : ℕ) / L = q := ⟨_, rfl⟩
    have hdm : L * q + (e : ℕ) % L = (e : ℕ) := by rw [← hq]; exact Nat.div_add_mod _ _
    have h2 : q < 2 := by rw [← hq]; exact pathNum_lt e
    have hm := posNum_lt e
    rw [pathFlow_apply]
    interval_cases q
    · rw [if_pos (by omega)]
      exact flow_eq_base hfeas 0 (by omega) (e : ℕ) (by omega) e ⟨0, by omega⟩
        (by omega) (by simp)
    · rw [if_neg (by omega)]
      have h1 : x e = x (⟨L, by omega⟩ : Fin (2 * L)) :=
        flow_eq_base hfeas 1 (by omega) ((e : ℕ) % L) hm e ⟨L, by omega⟩ (by omega) (by simp)
      rw [h1]
      linarith
  · rintro ⟨t, rfl⟩
    exact feasible_pathFlow hL t

/-! ### Energy -/

private theorem sum_pathSplit (L : ℕ) (a b : ℝ) :
    ∑ e : Fin (2 * L), (if (e : ℕ) < L then a else b) = L * a + L * b := by
  have hre : ∑ e : Fin (2 * L), (if (e : ℕ) < L then a else b)
      = ∑ k ∈ Finset.range (2 * L), (if k < L then a else b) :=
    Fin.sum_univ_eq_sum_range (fun k => if k < L then a else b) (2 * L)
  have hlo : ∀ k ∈ Finset.Ico 0 L, (if k < L then a else b) = a :=
    fun k hk => if_pos (Finset.mem_Ico.mp hk).2
  have hhi : ∀ k ∈ Finset.Ico L (2 * L), (if k < L then a else b) = b := by
    intro k hk
    exact if_neg (by have := (Finset.mem_Ico.mp hk).1; omega)
  rw [hre, Finset.range_eq_Ico,
    ← Finset.sum_Ico_consecutive _ (Nat.zero_le L) (by omega : L ≤ 2 * L),
    Finset.sum_congr rfl hlo, Finset.sum_congr rfl hhi, Finset.sum_const, Finset.sum_const,
    Nat.card_Ico, Nat.card_Ico, Nat.sub_zero, show 2 * L - L = L by omega,
    nsmul_eq_mul, nsmul_eq_mul]

private theorem edgeEnergy_one (y : ℝ) : edgeEnergy 1 1 y = |y| ^ 3 / 3 := by
  unfold edgeEnergy; split <;> ring

private theorem edgeLaw_one (y : ℝ) : edgeLaw 1 1 y = y * |y| := by
  unfold edgeLaw; split <;> ring

/-- The energy of a path-constant flow. -/
theorem energy_pathFlow (L : ℕ) (s t : ℝ) :
    (net L).energy (pathFlow L s t) = (L : ℝ) / 3 * (|s| ^ 3 + |t| ^ 3) := by
  have hterm : ∀ e : Fin (2 * L),
      edgeEnergy ((net L).positive e) ((net L).negative e) (pathFlow L s t e)
        = if (e : ℕ) < L then |s| ^ 3 / 3 else |t| ^ 3 / 3 := by
    intro e
    rw [positive_apply, negative_apply, pathFlow_apply, edgeEnergy_one]
    split <;> rfl
  rw [Network.energy, Finset.sum_congr rfl (fun e _ => hterm e), sum_pathSplit]
  ring

/-- The constant-one flow has energy `2 L / 3`. -/
theorem energy_one (L : ℕ) : (net L).energy (pathFlow L 1 1) = 2 * L / 3 := by
  rw [energy_pathFlow, abs_one]
  ring

/-! ### The physical flow -/

/-- All coefficients of the two-path network are strictly positive. -/
theorem net_positive (L : ℕ) : (net L).Positive := ⟨fun _ => one_pos, fun _ => one_pos⟩

/-- The integral potentials realize the edge laws of the constant-one flow. -/
theorem drops_eq_edgeLaw (L : ℕ) :
    (net L).drops (potential L) =
      fun e => edgeLaw ((net L).positive e) ((net L).negative e) (pathFlow L 1 1 e) := by
  funext e
  rw [drops_potential, positive_apply, negative_apply, pathFlow_one_apply, edgeLaw_one]
  norm_num

/-- The constant-one flow is conserved. -/
theorem feasible_one (L : ℕ) (hL : 0 < L) : (net L).Feasible (nom L) (pathFlow L 1 1) := by
  have h := feasible_pathFlow hL 1
  rwa [show (2 : ℝ) - 1 = 1 by norm_num] at h

/-- The constant-one flow minimizes the energy over all conserved flows. -/
theorem one_minimizer (L : ℕ) (hL : 0 < L) :
    ∀ y, (net L).Feasible (nom L) y → (net L).energy (pathFlow L 1 1) ≤ (net L).energy y :=
  (net L).physical_flow_minimizer (net_positive L) (feasible_one L hL) (drops_eq_edgeLaw L)

/-- Any conserved energy minimizer is the constant-one flow. -/
theorem eq_pathFlow_one_of_minimizer (L : ℕ) (hL : 0 < L) {x : Fin (2 * L) → ℝ}
    (hx : (net L).Feasible (nom L) x)
    (hmin : ∀ z, (net L).Feasible (nom L) z → (net L).energy x ≤ (net L).energy z) :
    x = pathFlow L 1 1 :=
  (net L).energy_minimizer_unique (net_positive L) hx (feasible_one L hL) hmin
    (one_minimizer L hL)

/-- Any conserved flow satisfying the edge laws is the constant-one flow. -/
theorem eq_pathFlow_one_of_physical (L : ℕ) (hL : 0 < L) {x : Fin (2 * L) → ℝ}
    (hx : (net L).Feasible (nom L) x)
    (hp : ∃ p, (net L).drops p =
      fun e => edgeLaw ((net L).positive e) ((net L).negative e) (x e)) :
    x = pathFlow L 1 1 := by
  obtain ⟨p, hp⟩ := hp
  exact eq_pathFlow_one_of_minimizer L hL hx
    ((net L).physical_flow_minimizer (net_positive L) hx hp)

/-- The two-path network has exactly one physical flow. -/
theorem exists_unique_physical (L : ℕ) (hL : 0 < L) :
    ∃! x : Fin (2 * L) → ℝ, (net L).Feasible (nom L) x ∧
      ∃ p, (net L).drops p =
        fun e => edgeLaw ((net L).positive e) ((net L).negative e) (x e) :=
  (net L).exists_unique_physical_flow (nom L) (net_positive L) _ (feasible_one L hL)

/-- The two-path network has exactly one energy minimizer. -/
theorem exists_unique_minimizer (L : ℕ) (hL : 0 < L) :
    ∃! x : Fin (2 * L) → ℝ, (net L).Feasible (nom L) x ∧
      ∀ z, (net L).Feasible (nom L) z → (net L).energy x ≤ (net L).energy z :=
  (net L).exists_unique_energy_minimizer (nom L) (net_positive L) _ (feasible_one L hL)

/-! ### Energy along the conserved family -/

/-- The energy of the conserved flow with path values `t` and `2 - t`. -/
def familyEnergy (L : ℕ) (t : ℝ) : ℝ := (net L).energy (pathFlow L t (2 - t))

/-- Closed form of the energy along the conserved family. -/
theorem familyEnergy_eq (L : ℕ) (t : ℝ) :
    familyEnergy L t = (L : ℝ) / 3 * (|t| ^ 3 + |2 - t| ^ 3) := energy_pathFlow L t (2 - t)

private theorem strictMono_mulAbs : StrictMono fun x : ℝ => x * |x| := by
  intro a b hab
  rcases le_or_gt 0 a with ha | ha
  · have hb : 0 < b := lt_of_le_of_lt ha hab
    simp only [abs_of_nonneg ha, abs_of_pos hb]
    nlinarith
  · rcases le_or_gt 0 b with hb | hb
    · simp only [abs_of_neg ha, abs_of_nonneg hb]
      nlinarith
    · simp only [abs_of_neg ha, abs_of_neg hb]
      nlinarith

/-- The derivative of the family energy. -/
theorem hasDerivAt_familyEnergy (L : ℕ) (t : ℝ) :
    HasDerivAt (familyEnergy L) ((L : ℝ) * (t * |t| - (2 - t) * |2 - t|)) t := by
  have hfun : familyEnergy L = fun s : ℝ =>
      (L : ℝ) * edgeEnergy 1 1 s + (L : ℝ) * edgeEnergy 1 1 (2 - s) := by
    funext s
    rw [familyEnergy_eq, edgeEnergy_one, edgeEnergy_one]
    ring
  rw [hfun]
  have h1 : HasDerivAt (fun s : ℝ => (L : ℝ) * edgeEnergy 1 1 s) ((L : ℝ) * (t * |t|)) t := by
    have h := (hasDerivAt_edgeEnergy 1 1 t).const_mul (L : ℝ)
    rwa [edgeLaw_one] at h
  have h2 : HasDerivAt (fun s : ℝ => (L : ℝ) * edgeEnergy 1 1 (2 - s))
      ((L : ℝ) * ((2 - t) * |2 - t| * (-1))) t := by
    have h := ((hasDerivAt_edgeEnergy 1 1 (2 - t)).comp t
      (by simpa using (hasDerivAt_id t).const_sub 2)).const_mul (L : ℝ)
    rwa [edgeLaw_one] at h
  rw [show (L : ℝ) * (t * |t| - (2 - t) * |2 - t|)
      = (L : ℝ) * (t * |t|) + (L : ℝ) * ((2 - t) * |2 - t| * (-1)) by ring]
  exact h1.add h2

/-- The family energy is continuous. -/
theorem continuous_familyEnergy (L : ℕ) : Continuous (familyEnergy L) :=
  continuous_iff_continuousAt.mpr fun t => (hasDerivAt_familyEnergy L t).continuousAt

/-- The family energy is strictly convex. -/
theorem familyEnergy_strictConvexOn (L : ℕ) (hL : 0 < L) :
    StrictConvexOn ℝ Set.univ (familyEnergy L) := by
  have hderiv : deriv (familyEnergy L) =
      fun t : ℝ => (L : ℝ) * (t * |t| - (2 - t) * |2 - t|) :=
    funext fun t => (hasDerivAt_familyEnergy L t).deriv
  refine StrictMono.strictConvexOn_univ_of_deriv (continuous_familyEnergy L) ?_
  rw [hderiv]
  intro s u hsu
  have hLR : (0 : ℝ) < L := by exact_mod_cast hL
  have h1 : s * |s| < u * |u| := strictMono_mulAbs hsu
  have h2 : (2 - u) * |2 - u| < (2 - s) * |2 - s| := strictMono_mulAbs (by linarith)
  exact mul_lt_mul_of_pos_left (by linarith) hLR

/-- The family energy is symmetric about `t = 1`. -/
theorem familyEnergy_symm (L : ℕ) (r : ℝ) : familyEnergy L (1 + r) = familyEnergy L (1 - r) := by
  rw [familyEnergy_eq, familyEnergy_eq, show (2 : ℝ) - (1 + r) = 1 - r by ring,
    show (2 : ℝ) - (1 - r) = 1 + r by ring]
  ring

/-- The family energy is strictly increasing to the right of `t = 1`. -/
theorem familyEnergy_strictMonoOn (L : ℕ) (hL : 0 < L) :
    StrictMonoOn (familyEnergy L) (Set.Ici 1) := by
  refine strictMonoOn_of_deriv_pos (convex_Ici 1) (continuous_familyEnergy L).continuousOn ?_
  intro s hs
  rw [interior_Ici] at hs
  have hs1 : (1 : ℝ) < s := hs
  have hd : deriv (familyEnergy L) s = (L : ℝ) * (s * |s| - (2 - s) * |2 - s|) :=
    (hasDerivAt_familyEnergy L s).deriv
  have hLR : (0 : ℝ) < L := by exact_mod_cast hL
  have h2 : (2 - s) * |2 - s| < s * |s| := strictMono_mulAbs (by linarith)
  rw [hd]
  exact mul_pos hLR (by linarith)

/-- Combined with `familyEnergy_symm`, the energy strictly increases with `|t - 1|`. -/
theorem familyEnergy_lt_of_le_of_lt (L : ℕ) (hL : 0 < L) {t₁ t₂ : ℝ}
    (h1 : 1 ≤ t₁) (h2 : t₁ < t₂) : familyEnergy L t₁ < familyEnergy L t₂ :=
  familyEnergy_strictMonoOn L hL h1 (le_of_lt (lt_of_le_of_lt h1 h2)) h2

/-! ### The certified gap of the trial flow -/

/-- The trial flow of the example belongs to the conserved family. -/
theorem pathFlow_trial (L : ℕ) (eps : ℝ) :
    pathFlow L (1 + eps) (1 - eps) = pathFlow L (1 + eps) (2 - (1 + eps)) := by
  rw [show (2 : ℝ) - (1 + eps) = 1 - eps by ring]

/-- The trial flow is conserved. -/
theorem feasible_trial (L : ℕ) (hL : 0 < L) (eps : ℝ) :
    (net L).Feasible (nom L) (pathFlow L (1 + eps) (1 - eps)) := by
  rw [pathFlow_trial]
  exact feasible_pathFlow hL (1 + eps)

/-- The exact energy of the trial flow. -/
theorem energy_trial (L : ℕ) {eps : ℝ} (h0 : 0 < eps) (h1 : eps < 1) :
    (net L).energy (pathFlow L (1 + eps) (1 - eps)) = 2 * L / 3 + 2 * L * eps ^ 2 := by
  rw [energy_pathFlow, abs_of_pos (by linarith : (0 : ℝ) < 1 + eps),
    abs_of_pos (by linarith : (0 : ℝ) < 1 - eps)]
  ring

/-- The exact energy gap of the trial flow is `2 L eps ^ 2`. -/
theorem gap_eq (L : ℕ) {eps : ℝ} (h0 : 0 < eps) (h1 : eps < 1) :
    (net L).energy (pathFlow L (1 + eps) (1 - eps)) - (net L).energy (pathFlow L 1 1)
      = 2 * L * eps ^ 2 := by
  rw [energy_trial L h0 h1, energy_one]
  ring

/-- The integral potentials pass the certificate root test with conjugate roots `1`. -/
theorem root_test (L : ℕ) (e : Fin (2 * L)) :
    |(net L).drops (potential L) e| ^ 3 ≤ ((fun _ => 1 : Fin (2 * L) → ℝ) e) ^ 2 *
      (if 0 ≤ (net L).drops (potential L) e then (net L).positive e
        else (net L).negative e) := by
  rw [drops_potential]
  norm_num

/-- The certificate's dual value is exactly the physical energy. -/
theorem dualLower_eq (L : ℕ) (hL : 0 < L) :
    (net L).dualLower (nom L) (potential L) (fun _ => 1) = 2 * L / 3 := by
  have hzero : ∀ c : Fin (2 * L), c ≠ ⟨0, by omega⟩ → c ≠ ⟨1, by omega⟩ →
      potential L c * nom L c = 0 := by
    intro c hc0 hc1
    have h0 : (c : ℕ) ≠ 0 := fun h => hc0 (Fin.ext h)
    have h1 : (c : ℕ) ≠ 1 := fun h => hc1 (Fin.ext h)
    simp [nom, h0, h1]
  have hpair : ∑ v : Fin (2 * L), potential L v * nom L v = 2 * L := by
    rw [sum_eq_pair _ (⟨0, by omega⟩ : Fin (2 * L)) (⟨1, by omega⟩ : Fin (2 * L))
      (by simp) hzero]
    simp [potential, nom]
    ring
  have hone : ∑ _e : Fin (2 * L), (1 : ℝ) = 2 * L := by simp
  rw [Network.dualLower, hpair, hone]
  ring

/-- The integral node potentials of the example, as exact integer data. -/
def intPotential (L : ℕ) : Fin (2 * L) → ℤ := fun v =>
  if (v : ℕ) = 0 then (L : ℤ)
  else if (v : ℕ) = 1 then 0
  else (L : ℤ) - 1 - ((((v : ℕ) - 2) % (L - 1) : ℕ) : ℤ)

theorem intPotential_cast (L : ℕ) :
    (fun v => (intPotential L v : ℝ)) = potential L := by
  funext v
  simp only [intPotential, potential]
  split_ifs <;> simp only [Int.cast_sub, Int.cast_one, Int.cast_zero, Int.cast_natCast]

/-- **CC33.**  The example's dual witnesses are exact data: the node potentials are
integral and the conjugate roots are rational, and their casts are precisely the
vectors used by `root_test`, `dualLower_eq` and `certified_gap_eq`. -/
theorem exists_integral_dual_witnesses (L : ℕ) :
    ∃ (p : Fin (2 * L) → ℤ) (u : Fin (2 * L) → ℚ),
      (fun v => (p v : ℝ)) = potential L ∧
      (fun e => (u e : ℝ)) = (fun _ => 1 : Fin (2 * L) → ℝ) :=
  ⟨intPotential L, fun _ => 1, intPotential_cast L, by funext e; norm_num⟩

/-- **CC33.**  The exact dual value `2 L / 3` is attained by integral potentials and
rational conjugate roots, so the certificate of the example is a rational witness. -/
theorem exists_integral_dualLower (L : ℕ) (hL : 0 < L) :
    ∃ (p : Fin (2 * L) → ℤ) (u : Fin (2 * L) → ℚ),
      (∀ e, |(net L).drops (fun v => (p v : ℝ)) e| ^ 3 ≤ ((u e : ℝ)) ^ 2 *
        (if 0 ≤ (net L).drops (fun v => (p v : ℝ)) e then (net L).positive e
          else (net L).negative e)) ∧
      (net L).dualLower (nom L) (fun v => (p v : ℝ)) (fun e => (u e : ℝ)) = 2 * L / 3 := by
  obtain ⟨p, u, hp, hu⟩ := exists_integral_dual_witnesses L
  have hu' : ∀ e, ((u e : ℚ) : ℝ) = 1 := fun e => congrFun hu e
  refine ⟨p, u, ?_, ?_⟩
  · intro e
    rw [hp]
    simpa [hu'] using root_test L e
  · rw [hp, hu]
    exact dualLower_eq L hL

/-- The certified gap of the trial flow equals its exact energy gap. -/
theorem certified_gap_eq (L : ℕ) (hL : 0 < L) {eps : ℝ} (h0 : 0 < eps) (h1 : eps < 1) :
    (net L).energy (pathFlow L (1 + eps) (1 - eps)) -
      (net L).dualLower (nom L) (potential L) (fun _ => 1) = 2 * L * eps ^ 2 := by
  rw [energy_trial L h0 h1, dualLower_eq L hL]
  ring

/-- The certificate is valid: its dual value bounds the energy of every conserved flow. -/
theorem dualLower_le (L : ℕ) {x : Fin (2 * L) → ℝ} (hx : (net L).Feasible (nom L) x) :
    (net L).dualLower (nom L) (potential L) (fun _ => 1) ≤ (net L).energy x :=
  (net L).dual_lower_bound (net_positive L) hx (fun _ => zero_le_one) (root_test L)

end

end PotentialFlow.TwoPath
