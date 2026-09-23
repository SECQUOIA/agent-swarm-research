import Formal.GridSwitching.Model
import Formal.GridSwitching.Endpoint
import Formal.GridSwitching.Compactness

/-!
# SC36 and SC37: the block-subset cost, the subset recurrence, and fixed-budget optimization

This module discharges the two tier-4 obligations of `topics/17-grid-switching/CLAIMS.md`
that concern the exact subset algorithm of
`paper-switching-control/sections/10-instance-algorithms.tex`.

## SC36 (`prop:subset-DP`)

Fix a grid `x` and grid-index boundaries `b` of `k` nominal blocks. For a mode `i` and a set
`U` of blocks, `blockSubsetCost x b A i U` is the cost `c_i(U)` of `eq:block-subset-cost`.

* `componentError_occupation_eq_blockSubsetCost`: `c_i(U)` is *exactly* the error contributed
  by mode `i` when the word assigns it precisely the blocks of `U`. Nothing forces `U` to be
  an interval, and `componentError_subsetWord` realizes an arbitrary, possibly disconnected,
  `U` by an explicit word. The proof is SC05: `Formal.GridSwitching.Endpoint` shows the error
  of a schedule is determined by its block endpoints, and `occupation_node` evaluates the
  occupation there as a prefix sum of block lengths.
* `blockSubsetCost_empty`: `c_i(∅) = m_i`, so unused modes still contribute.
* `D_occupation_eq_sup'_blockSubsetCost`: the error of a block schedule is the maximum over
  modes of the costs of their assigned block sets.
* `subsetDP`, `subsetDP_eq_iInf`, `subsetDP_eq_iInf_D`: the recurrence `eq:subset-DP` and the
  statement that `D_n([k])` is the optimum over *all* assignments of blocks to modes.

## SC37 (`thm:fixed-budget`)

The covering claim of the obligation has two clauses, and both are proved.

* `exists_isReduced_gridSchedule` is the first clause: every grid schedule with at most `s`
  switches has at most `k = min (s + 1, N)` maximal runs. "Maximal runs" is `IsReduced` of
  `Formal.GridSwitching.Model` — positive blocks, no two consecutive blocks sharing a mode —
  and the bound combines `exists_isReduced` with `card_positiveBlocks_comp_le`.
* `exists_blockPartition_of_isGridSchedule` is the second clause: such a schedule is the
  occupation of a word on exactly `k` nominal blocks with strictly increasing grid-index
  endpoints, and the subdivision does not change the control — the conclusion is an equality
  of occupations, not merely of errors. The proof is the source's run subdivision, carried out
  by counting distinct switch nodes.
* `isLeast_gridOPT_fixedBudget`: the exact fixed-budget grid optimum `gridOPT x A T s` is the
  least element of `fixedBudgetErrorSet`, the explicitly described finite family of errors
  indexed by block partitions and by assignments of blocks to modes.
* `ofReal_gridOPT_eq_iInf_subsetDP` combines the two obligations: the optimum is nonnegative,
  and it is the minimum, over block partitions, of the value of the subset recurrence.
* `card_subsetDP_states`, `card_subsetDP_transitions`, `card_blockPartitions`: the exact size
  recursions, `2 ^ k`, `3 ^ k` and `binom (N - 1, k - 1)`.
* `subsetDPStates`, `subsetDPTransitions`, `card_subsetDPStates`, `card_subsetDPTransitions`,
  `subsetDP_succ_eq_inf_transitions`: the first two of those counts restated about the DP's own
  states and transitions, with the transitions identified as the index set of `subsetDP_succ`.

## Representing `+∞`

The recurrence is stated in `ℝ≥0∞`. Block-subset costs are nonnegative reals, `ℝ≥0∞` is a
complete linear order, its top element is the `+∞` of `eq:subset-DP`, and — the reason it is
preferable to `WithTop ℝ` here — its bottom element `0` is exactly the value of the empty
maximum that the base case `D_0(∅) = 0` needs. Real costs enter through `ENNReal.ofReal`.

## Size recursions, and what is *not* claimed

`CLAIMS.md` excludes machine-level **bit**-complexity claims, and states that the verified
content of an algorithmic claim is its correctness, termination and exact arithmetic-operation
or size recursions. The two exclusions are kept apart here.

*Proved*: the exact sizes that `prop:subset-DP` and `eq:fixed-budget-complexity` sum over.
One mode's layer of `subsetDP` has exactly `2 ^ k` states (`card_subsetDP_states`, the `k 2^k`
term and the `O(n 2^k)` storage) and exactly `3 ^ k` state-transition pairs
(`card_subsetDP_transitions`, the source's `∑_{S ⊆ [k]} 2^{|S|} = 3^k`); the outer enumeration
has exactly `binom (N - 1, k - 1)` members (`card_blockPartitions`). The first two counts are
also stated about the DP's own objects, as `card_subsetDPStates` and
`card_subsetDPTransitions`, with `subsetDP_succ_eq_inf_transitions` identifying
`subsetDPTransitions` as the literal index set the recurrence minimizes over. Together with
`isLeast_gridOPT_fixedBudget`, which exhibits the optimum as a minimum over that explicit
finite index set, this is the structural content of the two bounds.

*Not claimed*: no bit-cost model, and no conversion of these sizes into a running time under
any execution model. Nothing below asserts a number of machine operations, a word size or a
rational bit length.

## Hypotheses added beyond the source

* `0 < n` wherever a maximum over modes must be nonempty, as elsewhere in the package.
* `0 < N` in the SC37 statements: with no grid cell there is no positive nominal block, the
  source's `k = min(s + 1, N)` is zero and its "subdivide until there are exactly `k` positive
  blocks" is vacuous. The source assumes a nondegenerate grid throughout.
* The block boundaries `b` in the SC36 statements are only assumed `Monotone`, which is weaker
  than the source's strictly increasing `b_0 < ... < b_k`; the SC37 enumeration
  `blockPartitions` does require strict monotonicity.
-/
namespace GridSwitching

open Set

variable {n N k : ℕ}

/-! ## Nominal blocks of a grid -/

/-- The length `ℓ_j = x_{b_j} - x_{b_{j-1}}` of the `j`-th nominal block. -/
def blockLength (x : Fin (N + 1) → ℝ) (b : Fin (k + 1) → Fin (N + 1)) (j : Fin k) : ℝ :=
  x (b j.succ) - x (b j.castSucc)

/-- The total length `∑_{h ∈ U, h ≤ j} ℓ_h` of the blocks of `U` completed by the node
`x_{b_j}`. Blocks are indexed from zero, so "`h ≤ j`" in the source's one-based indexing is
the condition `h < j` here. -/
noncomputable def prefixLength (x : Fin (N + 1) → ℝ) (b : Fin (k + 1) → Fin (N + 1))
    (U : Finset (Fin k)) (j : Fin (k + 1)) : ℝ :=
  ∑ h ∈ U.filter fun h : Fin k => h.val < j.val, blockLength x b h

@[simp] theorem prefixLength_empty (x : Fin (N + 1) → ℝ) (b : Fin (k + 1) → Fin (N + 1))
    (j : Fin (k + 1)) : prefixLength x b ∅ j = 0 := by
  simp [prefixLength]

@[simp] theorem prefixLength_zero (x : Fin (N + 1) → ℝ) (b : Fin (k + 1) → Fin (N + 1))
    (U : Finset (Fin k)) : prefixLength x b U 0 = 0 := by
  simp [prefixLength]

/-- At the final node every block of `U` has been completed. -/
theorem prefixLength_last (x : Fin (N + 1) → ℝ) (b : Fin (k + 1) → Fin (N + 1))
    (U : Finset (Fin k)) :
    prefixLength x b U (Fin.last k) = ∑ h ∈ U, blockLength x b h := by
  refine Finset.sum_congr (Finset.filter_true_of_mem fun h _ => ?_) fun _ _ => rfl
  simp

/-- The set of blocks that the word `p` assigns to the mode `i`. -/
def assignedBlocks (p : Fin k → Fin n) (i : Fin n) : Finset (Fin k) :=
  Finset.univ.filter fun j : Fin k => p j = i

@[simp] theorem mem_assignedBlocks {p : Fin k → Fin n} {i : Fin n} {j : Fin k} :
    j ∈ assignedBlocks p i ↔ p j = i := by
  simp [assignedBlocks]

/-- The occupation of a mode at a block endpoint is the total length of the blocks assigned to
it that are already complete. -/
theorem occupation_node {x : Fin (N + 1) → ℝ} (hx : Monotone x)
    {b : Fin (k + 1) → Fin (N + 1)} (hb : Monotone b) (p : Fin k → Fin n) (i : Fin n)
    (j : Fin (k + 1)) :
    occupation p (x ∘ b) i (x (b j)) = prefixLength x b (assignedBlocks p i) j := by
  rw [prefixLength, assignedBlocks, Finset.filter_filter, Finset.sum_filter]
  refine Finset.sum_congr rfl fun h _ => ?_
  simp only [Function.comp_apply]
  by_cases hp : p h = i
  · rcases lt_or_ge (h : ℕ) (j : ℕ) with hlt | hge
    · have h1 : b h.succ ≤ b j := hb (Fin.le_def.mpr (by simpa using hlt))
      have h2 : b h.castSucc ≤ b j := hb (Fin.le_def.mpr (by simp; omega))
      rw [if_pos hp, if_pos ⟨hp, hlt⟩, min_eq_right (hx h1), min_eq_right (hx h2), blockLength]
    · have h1 : b j ≤ b h.castSucc := hb (Fin.le_def.mpr (by simpa using hge))
      have h2 : b j ≤ b h.succ := hb (Fin.le_def.mpr (by simp; omega))
      rw [if_pos hp, if_neg (by simp [hp]; omega), min_eq_left (hx h1), min_eq_left (hx h2)]
      ring
  · rw [if_neg hp, if_neg (by simp [hp])]

/-! ## Component errors

`D` is a maximum over modes of the per-mode error, and SC36 is a statement about one mode at
a time, so the per-mode error is given a name here. -/

/-- The discrepancies of the single mode `i` over the horizon. -/
def componentErrorSet (A W : Fin n → ℝ → ℝ) (T : ℝ) (i : Fin n) : Set ℝ :=
  {e | ∃ t ∈ Icc (0 : ℝ) T, e = |A i t - W i t|}

/-- The error contributed by the single mode `i`. -/
noncomputable def componentError (A W : Fin n → ℝ → ℝ) (T : ℝ) (i : Fin n) : ℝ :=
  sSup (componentErrorSet A W T i)

theorem componentErrorSet_subset_errorSet (A W : Fin n → ℝ → ℝ) (T : ℝ) (i : Fin n) :
    componentErrorSet A W T i ⊆ errorSet A W T := by
  rintro e ⟨t, ht, rfl⟩
  exact ⟨i, t, ht, rfl⟩

theorem componentErrorSet_bddAbove {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (i : Fin n) : BddAbove (componentErrorSet A W T i) :=
  (errorSet_bddAbove hA hW).mono (componentErrorSet_subset_errorSet A W T i)

/-- Every discrepancy of the mode `i` is bounded by its component error. -/
theorem le_componentError {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (i : Fin n) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    |A i t - W i t| ≤ componentError A W T i :=
  le_csSup (componentErrorSet_bddAbove hA hW i) ⟨t, ht, rfl⟩

/-- The component error is the least uniform bound on the discrepancies of the mode `i`. -/
theorem componentError_le {A W : Fin n → ℝ → ℝ} {T c : ℝ} {i : Fin n} (hc : 0 ≤ c)
    (h : ∀ t ∈ Icc (0 : ℝ) T, |A i t - W i t| ≤ c) : componentError A W T i ≤ c :=
  Real.sSup_le (by rintro e ⟨t, ht, rfl⟩; exact h t ht) hc

theorem componentErrorSet_nonempty (A W : Fin n → ℝ → ℝ) {T : ℝ} (hT : 0 ≤ T) (i : Fin n) :
    (componentErrorSet A W T i).Nonempty :=
  ⟨|A i 0 - W i 0|, 0, ⟨le_rfl, hT⟩, rfl⟩

theorem componentError_le_D {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (hT : 0 ≤ T) (i : Fin n) : componentError A W T i ≤ D A W T :=
  csSup_le_csSup (errorSet_bddAbove hA hW) (componentErrorSet_nonempty A W hT i)
    (componentErrorSet_subset_errorSet A W T i)

theorem componentError_nonneg {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (hT : 0 ≤ T) (i : Fin n) : 0 ≤ componentError A W T i := by
  have h := le_componentError hA hW i (t := 0) ⟨le_rfl, hT⟩
  rwa [hA.initial, hW.initial, sub_zero, abs_zero] at h

/-- The full error is the maximum of the component errors. -/
theorem D_eq_sup'_componentError (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hW : IsCumulative W T) (hT : 0 ≤ T) :
    D A W T = Finset.univ.sup' ⟨⟨0, hn⟩, Finset.mem_univ _⟩ (componentError A W T) := by
  refine le_antisymm (D_le ?_ fun i t ht => ?_) (Finset.sup'_le _ _ fun i _ => ?_)
  · exact (componentError_nonneg hA hW hT ⟨0, hn⟩).trans
      (Finset.le_sup' (componentError A W T) (Finset.mem_univ _))
  · exact (le_componentError hA hW i ht).trans
      (Finset.le_sup' (componentError A W T) (Finset.mem_univ i))
  · exact componentError_le_D hA hW hT i

/-! ### SC05, per component

`Formal.GridSwitching.Endpoint` proves that the error of a schedule is determined by the
values at its block endpoints. The sandwich `exists_switchTime_sandwich` is already stated one
mode at a time, so the same argument gives the per-component form used below. -/

/-- SC05 for one component: the error of a single mode is at most `c` exactly when its
discrepancy is at most `c` at every switch time. -/
theorem componentError_le_iff_switchTimes {m : ℕ} (p : Fin m → Fin n) {τ : Fin (m + 1) → ℝ}
    {T : ℝ} (hτ : OrderedTimes τ T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) {c : ℝ}
    (hc : 0 ≤ c) (i : Fin n) :
    componentError A (occupation p τ) T i ≤ c ↔
      ∀ q : Fin (m + 1), |A i (τ q) - occupation p τ i (τ q)| ≤ c := by
  constructor
  · exact fun h q =>
      (le_componentError hA (occupation_isCumulative p hτ) i (hτ.mem_Icc q)).trans h
  · intro h
    refine componentError_le hc fun t ht => ?_
    obtain ⟨q₁, q₂, h₁, h₂⟩ := exists_switchTime_sandwich p hτ hA i ht
    have hb₁ := abs_le.mp (h q₁)
    have hb₂ := abs_le.mp (h q₂)
    rw [abs_le]
    constructor <;> linarith

/-- SC05 for one component, as an identity: the error of a single mode is the maximum of its
discrepancies at the switch times. -/
theorem componentError_eq_sup'_switchTimes {m : ℕ} (p : Fin m → Fin n) {τ : Fin (m + 1) → ℝ}
    {T : ℝ} (hτ : OrderedTimes τ T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (i : Fin n) :
    componentError A (occupation p τ) T i =
      Finset.univ.sup' ⟨0, Finset.mem_univ 0⟩
        fun q : Fin (m + 1) => |A i (τ q) - occupation p τ i (τ q)| := by
  set f : Fin (m + 1) → ℝ := fun q => |A i (τ q) - occupation p τ i (τ q)| with hf
  have hnonneg : (0 : ℝ) ≤ Finset.univ.sup' ⟨0, Finset.mem_univ 0⟩ f :=
    (abs_nonneg _).trans (Finset.le_sup' f (Finset.mem_univ (0 : Fin (m + 1))))
  refine le_antisymm ?_ (Finset.sup'_le _ _ fun q _ => ?_)
  · exact (componentError_le_iff_switchTimes p hτ hA hnonneg i).mpr
      fun q => Finset.le_sup' f (Finset.mem_univ q)
  · exact le_componentError hA (occupation_isCumulative p hτ) i (hτ.mem_Icc q)

/-! ## SC36, first half: the block-subset cost is the component error

`eq:block-subset-cost`. The maximum is taken over all `k + 1` block endpoints rather than over
the `k` interior ones of the source; the extra term at `j = 0` is `|A_i(0) - 0| = 0`, which
never exceeds a maximum of absolute values, so the two readings agree. -/

/-- The block-subset cost `c_i(U)` of `eq:block-subset-cost`: the largest deviation, over the
block endpoints, between the input's cumulative allocation to mode `i` and the total length of
the blocks of `U` completed so far. -/
noncomputable def blockSubsetCost (x : Fin (N + 1) → ℝ) (b : Fin (k + 1) → Fin (N + 1))
    (A : Fin n → ℝ → ℝ) (i : Fin n) (U : Finset (Fin k)) : ℝ :=
  Finset.univ.sup' ⟨0, Finset.mem_univ 0⟩
    fun j : Fin (k + 1) => |A i (x (b j)) - prefixLength x b U j|

theorem blockSubsetCost_nonneg (x : Fin (N + 1) → ℝ) (b : Fin (k + 1) → Fin (N + 1))
    (A : Fin n → ℝ → ℝ) (i : Fin n) (U : Finset (Fin k)) :
    0 ≤ blockSubsetCost x b A i U := by
  refine le_trans (abs_nonneg (A i (x (b 0)) - prefixLength x b U 0)) ?_
  exact Finset.le_sup' (fun j : Fin (k + 1) => |A i (x (b j)) - prefixLength x b U j|)
    (Finset.mem_univ 0)

/-- The term `j = 0` of `blockSubsetCost` vanishes, so the maximum agrees with the source's
maximum of `eq:block-subset-cost` over the interior endpoints `x_{b_1}, ..., x_{b_k}`. -/
theorem blockSubsetCost_eq_sup'_succ {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {b : Fin (k + 1) → Fin (N + 1)} (hb0 : b 0 = 0) {A : Fin n → ℝ → ℝ}
    (hA : IsCumulative A T) (i : Fin n) (U : Finset (Fin k)) (hk : 0 < k) :
    blockSubsetCost x b A i U =
      (Finset.univ : Finset (Fin k)).sup' ⟨⟨0, hk⟩, Finset.mem_univ _⟩
        fun j : Fin k => |A i (x (b j.succ)) - prefixLength x b U j.succ| := by
  set R : ℝ := (Finset.univ : Finset (Fin k)).sup' ⟨⟨0, hk⟩, Finset.mem_univ _⟩
    fun j : Fin k => |A i (x (b j.succ)) - prefixLength x b U j.succ| with hR
  have hR0 : 0 ≤ R := (abs_nonneg _).trans (Finset.le_sup'
    (fun j : Fin k => |A i (x (b j.succ)) - prefixLength x b U j.succ|)
    (Finset.mem_univ (⟨0, hk⟩ : Fin k)))
  refine le_antisymm (Finset.sup'_le _ _ fun j _ => ?_) (Finset.sup'_le _ _ fun j _ => ?_)
  · refine Fin.cases ?_ ?_ j
    · rw [hb0, hx.first, prefixLength_zero, hA.initial i, sub_zero, abs_zero]
      exact hR0
    · intro j'
      exact Finset.le_sup'
        (fun j : Fin k => |A i (x (b j.succ)) - prefixLength x b U j.succ|) (Finset.mem_univ j')
  · exact Finset.le_sup'
      (fun q : Fin (k + 1) => |A i (x (b q)) - prefixLength x b U q|) (Finset.mem_univ j.succ)

/-- Block boundaries are a family of ordered times. -/
theorem orderedTimes_comp_blockMap {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {b : Fin (k + 1) → Fin (N + 1)} (hb : Monotone b) (hb0 : b 0 = 0)
    (hbl : b (Fin.last k) = Fin.last N) : OrderedTimes (x ∘ b) T :=
  ⟨by simp only [Function.comp_apply, hb0, hx.first],
    by simp only [Function.comp_apply, hbl, hx.last], hx.strictMono.monotone.comp hb⟩

/-- SC36, first half: `c_i(U)` is exactly the error contributed by mode `i` when the word `p`
assigns it precisely the blocks of `U`. No connectivity of `U` is assumed. -/
theorem componentError_occupation_eq_blockSubsetCost {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {b : Fin (k + 1) → Fin (N + 1)} (hb : Monotone b) (hb0 : b 0 = 0)
    (hbl : b (Fin.last k) = Fin.last N) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T)
    (p : Fin k → Fin n) (i : Fin n) :
    componentError A (occupation p (x ∘ b)) T i =
      blockSubsetCost x b A i (assignedBlocks p i) := by
  rw [componentError_eq_sup'_switchTimes p (orderedTimes_comp_blockMap hx hb hb0 hbl) hA i,
    blockSubsetCost]
  refine Finset.sup'_congr _ rfl fun j _ => ?_
  rw [Function.comp_apply, occupation_node hx.strictMono.monotone hb p i j]

/-- The word that assigns exactly the blocks of `U` to the mode `i`. -/
def subsetWord (U : Finset (Fin k)) (i i' : Fin n) (j : Fin k) : Fin n :=
  if j ∈ U then i else i'

@[simp] theorem assignedBlocks_subsetWord {U : Finset (Fin k)} {i i' : Fin n} (hii : i' ≠ i) :
    assignedBlocks (subsetWord U i i') i = U := by
  ext j
  simp only [mem_assignedBlocks, subsetWord]
  by_cases hj : j ∈ U <;> simp [hj, hii]

/-- SC36, first half, for an arbitrary subset: every `U ⊆ [k]`, connected or not, is realized
as the block set of a mode, and then `c_i(U)` is that mode's component error. At least two
modes are needed to have somewhere to put the remaining blocks. -/
theorem componentError_subsetWord {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {b : Fin (k + 1) → Fin (N + 1)} (hb : Monotone b) (hb0 : b 0 = 0)
    (hbl : b (Fin.last k) = Fin.last N) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T)
    (U : Finset (Fin k)) {i i' : Fin n} (hii : i' ≠ i) :
    componentError A (occupation (subsetWord U i i') (x ∘ b)) T i = blockSubsetCost x b A i U := by
  rw [componentError_occupation_eq_blockSubsetCost hx hb hb0 hbl hA, assignedBlocks_subsetWord hii]

/-- SC36: the cost of the empty subset is the terminal mass, so unused modes still contribute
to the objective. -/
theorem blockSubsetCost_empty {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {b : Fin (k + 1) → Fin (N + 1)} (hb : Monotone b) (hbl : b (Fin.last k) = Fin.last N)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (i : Fin n) :
    blockSubsetCost x b A i (∅ : Finset (Fin k)) = masses A T i := by
  have hval : ∀ j : Fin (k + 1), |A i (x (b j)) - prefixLength x b (∅ : Finset (Fin k)) j|
      = A i (x (b j)) := by
    intro j
    rw [prefixLength_empty, sub_zero, abs_of_nonneg (hA.nonneg i (hx.mem_Icc (b j)))]
  have hlast : A i (x (b (Fin.last k))) = masses A T i := by
    rw [hbl, hx.last]; rfl
  refine le_antisymm (Finset.sup'_le _ _ fun j _ => ?_) ?_
  · rw [hval j, ← hlast]
    exact hA.mono i _ _ (hx.mem_Icc (b j)).1
      (hx.strictMono.monotone (hb (Fin.le_last j))) (hx.mem_Icc (b (Fin.last k))).2
  · rw [← hlast, ← hval (Fin.last k)]
    exact Finset.le_sup'
      (fun j : Fin (k + 1) => |A i (x (b j)) - prefixLength x b (∅ : Finset (Fin k)) j|)
      (Finset.mem_univ (Fin.last k))

/-- SC36: the error of a block schedule is the maximum over modes of the block-subset costs of
the sets of blocks assigned to them. -/
theorem D_occupation_eq_sup'_blockSubsetCost (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {b : Fin (k + 1) → Fin (N + 1)} (hb : Monotone b) (hb0 : b 0 = 0)
    (hbl : b (Fin.last k) = Fin.last N) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T)
    (p : Fin k → Fin n) :
    D A (occupation p (x ∘ b)) T =
      Finset.univ.sup' ⟨⟨0, hn⟩, Finset.mem_univ _⟩
        fun i => blockSubsetCost x b A i (assignedBlocks p i) := by
  rw [D_eq_sup'_componentError hn hA
    (occupation_isCumulative p (orderedTimes_comp_blockMap hx hb hb0 hbl)) hx.horizon_nonneg]
  refine Finset.sup'_congr (s := (Finset.univ : Finset (Fin n))) _ rfl fun i _ => ?_
  exact componentError_occupation_eq_blockSubsetCost hx hb hb0 hbl hA p i

/-! ## SC36, second half: the subset recurrence

`eq:subset-DP`. The value `+∞` of the source is represented by the top element of `ℝ≥0∞`:
the block-subset costs are nonnegative reals, `ℝ≥0∞` is a complete linear order whose bottom
element `0` is exactly the cost of the empty family of modes, and no `WithTop`/`WithBot`
bookkeeping is needed for the empty maxima that appear in the base case. -/

open scoped ENNReal

/-- The recurrence `eq:subset-DP`, for an abstract per-mode cost `c`. The natural number `m`
counts the modes already processed, so `c m` is the cost function of the `(m+1)`-st mode. -/
noncomputable def subsetDP (c : ℕ → Finset (Fin k) → ℝ≥0∞) : ℕ → Finset (Fin k) → ℝ≥0∞
  | 0, S => if S = ∅ then 0 else ⊤
  | m + 1, S => S.powerset.inf fun U => c m U ⊔ subsetDP c m (S \ U)

@[simp] theorem subsetDP_zero (c : ℕ → Finset (Fin k) → ℝ≥0∞) (S : Finset (Fin k)) :
    subsetDP c 0 S = if S = ∅ then 0 else ⊤ := rfl

theorem subsetDP_succ (c : ℕ → Finset (Fin k) → ℝ≥0∞) (m : ℕ) (S : Finset (Fin k)) :
    subsetDP c (m + 1) S = S.powerset.inf fun U => c m U ⊔ subsetDP c m (S \ U) := rfl

/-- The objective value of the assignment `g` of blocks to the first `m` modes: the largest
cost incurred by one of those modes. -/
noncomputable def dpAssignCost (c : ℕ → Finset (Fin k) → ℝ≥0∞) (m : ℕ) (S : Finset (Fin k))
    (g : Fin k → ℕ) : ℝ≥0∞ :=
  (Finset.range m).sup fun t => c t (S.filter fun j => g j = t)

/-- Peeling the last mode off an assignment objective. -/
theorem dpAssignCost_succ (c : ℕ → Finset (Fin k) → ℝ≥0∞) (m : ℕ) (S : Finset (Fin k))
    (g : Fin k → ℕ) :
    dpAssignCost c (m + 1) S g =
      c m (S.filter fun j => g j = m) ⊔
        dpAssignCost c m (S \ S.filter fun j => g j = m) g := by
  have hfil : ∀ t ∈ Finset.range m,
      (S \ S.filter fun j => g j = m).filter (fun j => g j = t) = S.filter fun j => g j = t := by
    intro t ht
    rw [Finset.mem_range] at ht
    ext j
    simp only [Finset.mem_filter, Finset.mem_sdiff]
    constructor
    · rintro ⟨⟨hj, -⟩, hgt⟩; exact ⟨hj, hgt⟩
    · rintro ⟨hj, hgt⟩
      exact ⟨⟨hj, fun hc => by have h2 := hc.2; omega⟩, hgt⟩
  simp only [dpAssignCost, Finset.range_add_one, Finset.sup_insert]
  congr 1
  exact Finset.sup_congr rfl fun t ht => congrArg _ (hfil t ht).symm

/-- One direction of SC36's recurrence: the dynamic program never exceeds the objective of any
assignment of the blocks of `S` to the first `m` modes. -/
theorem subsetDP_le_dpAssignCost (c : ℕ → Finset (Fin k) → ℝ≥0∞) :
    ∀ (m : ℕ) (S : Finset (Fin k)) (g : Fin k → ℕ), (∀ j ∈ S, g j < m) →
      subsetDP c m S ≤ dpAssignCost c m S g := by
  intro m
  induction m with
  | zero =>
    intro S g hg
    have hS : S = ∅ := Finset.eq_empty_of_forall_notMem fun j hj => absurd (hg j hj) (by omega)
    simp [hS]
  | succ m ih =>
    intro S g hg
    set U : Finset (Fin k) := S.filter fun j => g j = m with hU
    have hUS : U ∈ S.powerset := Finset.mem_powerset.mpr (Finset.filter_subset _ _)
    have hrest : ∀ j ∈ S \ U, g j < m := by
      intro j hj
      rw [Finset.mem_sdiff, hU, Finset.mem_filter] at hj
      have h1 := hg j hj.1
      have h2 : g j ≠ m := fun hc => hj.2 ⟨hj.1, hc⟩
      omega
    calc subsetDP c (m + 1) S ≤ c m U ⊔ subsetDP c m (S \ U) := by
          rw [subsetDP_succ]; exact Finset.inf_le hUS
      _ ≤ c m U ⊔ dpAssignCost c m (S \ U) g := sup_le_sup_left (ih (S \ U) g hrest) _
      _ = dpAssignCost c (m + 1) S g := (dpAssignCost_succ c m S g).symm

/-- The other direction of SC36's recurrence: unless it is `+∞`, the value of the dynamic
program is the objective of an explicit assignment. This is the traceback of the source. -/
theorem exists_dpAssignCost_le_subsetDP (c : ℕ → Finset (Fin k) → ℝ≥0∞) :
    ∀ (m : ℕ) (S : Finset (Fin k)), subsetDP c m S = ⊤ ∨
      ∃ g : Fin k → ℕ, (∀ j ∈ S, g j < m) ∧ dpAssignCost c m S g ≤ subsetDP c m S := by
  intro m
  induction m with
  | zero =>
    intro S
    by_cases hS : S = ∅
    · refine Or.inr ⟨fun _ => 0, ?_, ?_⟩
      · intro j hj; rw [hS] at hj; exact absurd hj (Finset.notMem_empty j)
      · simp [dpAssignCost, hS]
    · exact Or.inl (by simp [hS])
  | succ m ih =>
    intro S
    obtain ⟨U, hU, hUeq⟩ := Finset.exists_mem_eq_inf S.powerset ⟨∅, Finset.empty_mem_powerset S⟩
      fun U => c m U ⊔ subsetDP c m (S \ U)
    have hUS : U ⊆ S := Finset.mem_powerset.mp hU
    have hval : subsetDP c (m + 1) S = c m U ⊔ subsetDP c m (S \ U) := by
      rw [subsetDP_succ]; exact hUeq
    rcases ih (S \ U) with htop | ⟨g, hgval, hgle⟩
    · exact Or.inl (by rw [hval, htop, sup_top_eq])
    · refine Or.inr ⟨fun j => if j ∈ U then m else g j, ?_, ?_⟩
      · intro j hj
        by_cases hjU : j ∈ U
        · simp [hjU]
        · have : g j < m := hgval j (Finset.mem_sdiff.mpr ⟨hj, hjU⟩)
          simp [hjU]; omega
      · have hfilm : (S.filter fun j => (if j ∈ U then m else g j) = m) = U := by
          ext j
          simp only [Finset.mem_filter]
          constructor
          · rintro ⟨hj, hgj⟩
            by_contra hjU
            rw [if_neg hjU] at hgj
            exact absurd (hgval j (Finset.mem_sdiff.mpr ⟨hj, hjU⟩)) (by omega)
          · intro hjU
            exact ⟨hUS hjU, by simp [hjU]⟩
        have hrestr : dpAssignCost c m (S \ U) (fun j => if j ∈ U then m else g j)
            = dpAssignCost c m (S \ U) g := by
          refine Finset.sup_congr rfl fun t _ => congrArg _ ?_
          refine Finset.filter_congr fun j hj => ?_
          simp only [Finset.mem_sdiff] at hj
          simp only [if_neg hj.2]
        rw [dpAssignCost_succ, hfilm, hrestr, hval]
        exact sup_le_sup_left hgle _

/-- SC36, `eq:subset-DP`: the dynamic program computes the minimum, over all assignments of the
blocks of `S` to the first `m` modes, of the largest cost incurred by one of those modes. -/
theorem subsetDP_eq_iInf (c : ℕ → Finset (Fin k) → ℝ≥0∞) (m : ℕ) (S : Finset (Fin k)) :
    subsetDP c m S = ⨅ g ∈ {g : Fin k → ℕ | ∀ j ∈ S, g j < m}, dpAssignCost c m S g := by
  refine le_antisymm (le_iInf fun g => le_iInf fun hg => subsetDP_le_dpAssignCost c m S g hg) ?_
  rcases exists_dpAssignCost_le_subsetDP c m S with htop | ⟨g, hg, hle⟩
  · rw [htop]; exact le_top
  · exact le_trans (iInf_le_of_le g (iInf_le_of_le hg le_rfl)) hle

/-! ### The recurrence applied to the block-subset costs -/

/-- The per-mode cost fed to the recurrence: the block-subset cost of `eq:block-subset-cost`
for the mode with index `t`, and `+∞` for indices beyond the mode count. -/
noncomputable def modeCost (x : Fin (N + 1) → ℝ) (b : Fin (k + 1) → Fin (N + 1))
    (A : Fin n → ℝ → ℝ) (t : ℕ) (U : Finset (Fin k)) : ℝ≥0∞ :=
  if h : t < n then ENNReal.ofReal (blockSubsetCost x b A ⟨t, h⟩ U) else ⊤

/-- The objective of an assignment of all blocks to all modes is the error of the corresponding
block schedule. -/
theorem dpAssignCost_modeCost (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {b : Fin (k + 1) → Fin (N + 1)} (hb : Monotone b) (hb0 : b 0 = 0)
    (hbl : b (Fin.last k) = Fin.last N) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T)
    (p : Fin k → Fin n) :
    dpAssignCost (modeCost x b A) n Finset.univ (fun j => (p j : ℕ))
      = ENNReal.ofReal (D A (occupation p (x ∘ b)) T) := by
  set F : Fin n → ℝ := fun i => blockSubsetCost x b A i (assignedBlocks p i) with hF
  have hmode : ∀ i : Fin n,
      modeCost x b A (i : ℕ)
          (Finset.univ.filter fun j : Fin k => (p j : ℕ) = (i : ℕ)) = ENNReal.ofReal (F i) := by
    intro i
    have h1 : (Finset.univ.filter fun j : Fin k => (p j : ℕ) = (i : ℕ)) = assignedBlocks p i := by
      ext j
      simp [assignedBlocks, Fin.ext_iff]
    rw [modeCost, dif_pos i.isLt, h1, Fin.eta]
  rw [D_occupation_eq_sup'_blockSubsetCost hn hx hb hb0 hbl hA p, dpAssignCost, ← hF]
  refine le_antisymm (Finset.sup_le fun t ht => ?_) ?_
  · rw [Finset.mem_range] at ht
    rw [hmode ⟨t, ht⟩]
    exact ENNReal.ofReal_le_ofReal (Finset.le_sup' F (Finset.mem_univ _))
  · obtain ⟨i₀, -, hi₀⟩ := Finset.exists_mem_eq_sup'
      (⟨⟨0, hn⟩, Finset.mem_univ _⟩ : (Finset.univ : Finset (Fin n)).Nonempty) F
    rw [hi₀, ← hmode i₀]
    exact Finset.le_sup (f := fun t => modeCost x b A t
      (Finset.univ.filter fun j : Fin k => (p j : ℕ) = t)) (Finset.mem_range.mpr i₀.isLt)

/-- SC36, `eq:subset-DP`: started from `D_0(∅) = 0` and `D_0(S) = +∞` for `S ≠ ∅`, the
recurrence computes at `D_n([k])` the exact optimum over all assignments of the `k` nominal
blocks to the `n` modes, the objective of an assignment being the error of the corresponding
block schedule. -/
theorem subsetDP_eq_iInf_D (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {b : Fin (k + 1) → Fin (N + 1)} (hb : Monotone b) (hb0 : b 0 = 0)
    (hbl : b (Fin.last k) = Fin.last N) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) :
    subsetDP (modeCost x b A) n Finset.univ
      = ⨅ p : Fin k → Fin n, ENNReal.ofReal (D A (occupation p (x ∘ b)) T) := by
  refine le_antisymm (le_iInf fun p => ?_) ?_
  · rw [← dpAssignCost_modeCost hn hx hb hb0 hbl hA p]
    exact subsetDP_le_dpAssignCost _ n _ _ fun j _ => (p j).isLt
  · rcases exists_dpAssignCost_le_subsetDP (modeCost x b A) n Finset.univ with htop | ⟨g, hg, hle⟩
    · rw [htop]; exact le_top
    · have hp : ∀ j : Fin k, g j < n := fun j => hg j (Finset.mem_univ j)
      refine le_trans (iInf_le _ fun j => (⟨g j, hp j⟩ : Fin n)) ?_
      rw [← dpAssignCost_modeCost hn hx hb hb0 hbl hA fun j => (⟨g j, hp j⟩ : Fin n)]
      exact hle

/-! ## SC37, step 1: nominal blocks and the cells they contain

`thm:fixed-budget` compares a grid schedule with the finer schedule that treats every grid
cell as its own block. The two have the same occupation, because the cells of a nominal block
tile it. -/

/-- Telescoping a difference over a range of natural numbers. -/
private theorem sum_Ico_telescope' (f : ℕ → ℝ) {u v : ℕ} (huv : u ≤ v) :
    ∑ w ∈ Finset.Ico u v, (f (w + 1) - f w) = f v - f u := by
  induction v, huv using Nat.le_induction with
  | base => simp
  | succ v hv ih => rw [Finset.sum_Ico_succ_top hv, ih]; ring

/-- The clipped occupation of a stretch of the grid is the sum of the clipped occupations of
its cells. -/
private theorem sum_cells_eq {x : Fin (N + 1) → ℝ} (t : ℝ) {q q' : Fin (N + 1)}
    (hq : (q : ℕ) ≤ (q' : ℕ)) :
    (∑ u : Fin N, if (q : ℕ) ≤ (u : ℕ) ∧ (u : ℕ) < (q' : ℕ) then
        min t (x u.succ) - min t (x u.castSucc) else 0)
      = min t (x q') - min t (x q) := by
  set X : ℕ → ℝ := fun w => min t (x ⟨min w N, Nat.lt_succ_of_le (min_le_right _ _)⟩) with hX
  have hXnode : ∀ r : Fin (N + 1), X (r : ℕ) = min t (x r) := by
    intro r
    simp only [hX]
    congr 2
    exact Fin.ext (by simpa using Nat.min_eq_left (Nat.lt_succ_iff.mp r.isLt))
  have hXcast : ∀ u : Fin N, X (u : ℕ) = min t (x u.castSucc) := by
    intro u
    simpa using hXnode u.castSucc
  have hXsucc : ∀ u : Fin N, X ((u : ℕ) + 1) = min t (x u.succ) := by
    intro u
    have := hXnode u.succ
    rwa [Fin.val_succ] at this
  have hrange : ((Finset.range N).filter fun w => (q : ℕ) ≤ w ∧ w < (q' : ℕ))
      = Finset.Ico (q : ℕ) (q' : ℕ) := by
    ext w
    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_Ico]
    have hq'N : (q' : ℕ) ≤ N := Nat.lt_succ_iff.mp q'.isLt
    omega
  calc (∑ u : Fin N, if (q : ℕ) ≤ (u : ℕ) ∧ (u : ℕ) < (q' : ℕ) then
          min t (x u.succ) - min t (x u.castSucc) else 0)
      = ∑ u : Fin N, if (q : ℕ) ≤ (u : ℕ) ∧ (u : ℕ) < (q' : ℕ) then
          X ((u : ℕ) + 1) - X (u : ℕ) else 0 := by
        refine Finset.sum_congr rfl fun u _ => ?_
        rw [hXcast u, hXsucc u]
    _ = ∑ w ∈ Finset.range N, if (q : ℕ) ≤ w ∧ w < (q' : ℕ) then X (w + 1) - X w else 0 :=
        Fin.sum_univ_eq_sum_range
          (fun w => if (q : ℕ) ≤ w ∧ w < (q' : ℕ) then X (w + 1) - X w else 0) N
    _ = ∑ w ∈ Finset.Ico (q : ℕ) (q' : ℕ), (X (w + 1) - X w) := by
        rw [← Finset.sum_filter, hrange]
    _ = min t (x q') - min t (x q) := by
        rw [sum_Ico_telescope' X hq, hXnode, hXnode]

/-- A cell lies in at most one nominal block. -/
theorem block_unique {m : ℕ} {g : Fin (m + 1) → Fin (N + 1)} (hg : Monotone g) {u : ℕ}
    {j j' : Fin m} (h : (g j.castSucc : ℕ) ≤ u ∧ u < (g j.succ : ℕ))
    (h' : (g j'.castSucc : ℕ) ≤ u ∧ u < (g j'.succ : ℕ)) : j = j' := by
  rcases lt_trichotomy j j' with hlt | heq | hlt
  · have hle : g j.succ ≤ g j'.castSucc := by
      refine hg (Fin.le_def.mpr ?_)
      simp only [Fin.val_succ, Fin.val_castSucc]
      omega
    have := Fin.le_def.mp hle
    omega
  · exact heq
  · have hle : g j'.succ ≤ g j.castSucc := by
      refine hg (Fin.le_def.mpr ?_)
      simp only [Fin.val_succ, Fin.val_castSucc]
      omega
    have := Fin.le_def.mp hle
    omega

/-- Subdividing a schedule's nominal blocks into grid cells does not change its occupation:
a word with monotone grid-index boundaries has the occupation of the cellwise word it
induces. -/
theorem occupation_blockMap {m : ℕ} (x : Fin (N + 1) → ℝ) {g : Fin (m + 1) → Fin (N + 1)}
    (hg : Monotone g) (p : Fin m → Fin n) {β : Fin N → Fin m}
    (hβ : ∀ u : Fin N, (g (β u).castSucc : ℕ) ≤ (u : ℕ) ∧ (u : ℕ) < (g (β u).succ : ℕ)) :
    occupation p (x ∘ g) = occupation (fun u => p (β u)) x := by
  funext i t
  have hexpand : ∀ j : Fin m,
      (if p j = i then min t (x (g j.succ)) - min t (x (g j.castSucc)) else 0)
        = ∑ u : Fin N, if p j = i ∧ ((g j.castSucc : ℕ) ≤ (u : ℕ) ∧
            (u : ℕ) < (g j.succ : ℕ)) then min t (x u.succ) - min t (x u.castSucc) else 0 := by
    intro j
    have hjle : (g j.castSucc : ℕ) ≤ (g j.succ : ℕ) :=
      Fin.le_def.mp (hg (Fin.castSucc_le_succ j))
    by_cases hp : p j = i
    · simp only [hp, true_and, if_true]
      rw [sum_cells_eq t hjle]
    · simp [hp]
  have hcollapse : ∀ u : Fin N,
      (∑ j : Fin m, if p j = i ∧ ((g j.castSucc : ℕ) ≤ (u : ℕ) ∧
          (u : ℕ) < (g j.succ : ℕ)) then min t (x u.succ) - min t (x u.castSucc) else 0)
        = if p (β u) = i then min t (x u.succ) - min t (x u.castSucc) else 0 := by
    intro u
    rw [Finset.sum_eq_single (β u)]
    · rw [if_congr (and_iff_left (hβ u)) rfl rfl]
    · intro j _ hne
      refine if_neg fun hc => hne ?_
      exact block_unique hg hc.2 (hβ u)
    · intro hc
      exact absurd (Finset.mem_univ (β u)) hc
  simp only [occupation, Function.comp_apply]
  rw [Finset.sum_congr rfl fun j _ => hexpand j, Finset.sum_comm]
  exact Finset.sum_congr rfl fun u _ => hcollapse u

/-- The number of nominal blocks entirely completed by the end of the cell `u`. -/
private noncomputable def blockCount {m : ℕ} (g : Fin (m + 1) → Fin (N + 1)) (u : ℕ) : ℕ :=
  ((Finset.univ : Finset (Fin m)).filter fun j : Fin m => (g j.succ : ℕ) ≤ u).card

private theorem card_filter_val_lt (m r : ℕ) (hr : r ≤ m) :
    ((Finset.univ : Finset (Fin m)).filter fun j : Fin m => (j : ℕ) < r).card = r := by
  rw [← Finset.card_image_of_injective _ (Fin.val_injective (n := m))]
  rw [show ((Finset.univ : Finset (Fin m)).filter fun j : Fin m => (j : ℕ) < r).image Fin.val
      = Finset.range r from ?_]
  · exact Finset.card_range r
  · ext w
    simp only [Finset.mem_image, Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_range]
    constructor
    · rintro ⟨j, hj, rfl⟩; exact hj
    · intro hw; exact ⟨⟨w, by omega⟩, hw, rfl⟩

/-- Every grid cell lies in a nominal block of a monotone boundary family that starts at the
first grid node and ends at the last. -/
theorem exists_blockMap {m : ℕ} {g : Fin (m + 1) → Fin (N + 1)} (hg : Monotone g)
    (hg0 : g 0 = 0) (hgl : g (Fin.last m) = Fin.last N) :
    ∃ β : Fin N → Fin m, ∀ u : Fin N,
      (g (β u).castSucc : ℕ) ≤ (u : ℕ) ∧ (u : ℕ) < (g (β u).succ : ℕ) := by
  have hdown : ∀ (w : ℕ) (j j' : Fin m), j ≤ j' → (g j'.succ : ℕ) ≤ w →
      (g j.succ : ℕ) ≤ w := fun w j j' hjj hle =>
    le_trans (Fin.le_def.mp (hg (Fin.succ_le_succ_iff.mpr hjj))) hle
  have hup : ∀ (w : ℕ) (j₀ : Fin m), ¬ ((g j₀.succ : ℕ) ≤ w) → blockCount g w ≤ (j₀ : ℕ) := by
    intro w j₀ hnot
    have hsub : ((Finset.univ : Finset (Fin m)).filter fun j : Fin m => (g j.succ : ℕ) ≤ w)
        ⊆ (Finset.univ : Finset (Fin m)).filter fun j : Fin m => (j : ℕ) < (j₀ : ℕ) := by
      intro j hj
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hj ⊢
      by_contra hc
      exact hnot (hdown w j₀ j (Fin.le_def.mpr (by omega)) hj)
    calc blockCount g w
        ≤ ((Finset.univ : Finset (Fin m)).filter fun j : Fin m => (j : ℕ) < (j₀ : ℕ)).card :=
          Finset.card_le_card hsub
      _ = (j₀ : ℕ) := card_filter_val_lt m (j₀ : ℕ) (le_of_lt j₀.isLt)
  have hmpos : Fin N → 0 < m := by
    intro u
    have hu : (u : ℕ) < N := u.isLt
    rcases Nat.eq_zero_or_pos m with hm0 | hm
    · exfalso
      subst hm0
      have h1 : (0 : Fin (N + 1)) = Fin.last N := by
        rw [← hg0, ← hgl]
        exact congrArg g (Fin.ext (by simp))
      have h2 : (0 : ℕ) = N := congrArg Fin.val h1
      omega
    · exact hm
  have hlt : ∀ u : Fin N, blockCount g (u : ℕ) < m := by
    intro u
    have hu : (u : ℕ) < N := u.isLt
    have hm := hmpos u
    have hnot : ¬ ((g (⟨m - 1, by omega⟩ : Fin m).succ : ℕ) ≤ (u : ℕ)) := by
      have hsucc : (⟨m - 1, by omega⟩ : Fin m).succ = Fin.last m := by
        refine Fin.ext ?_
        simp only [Fin.val_succ, Fin.val_last]
        omega
      rw [hsucc, hgl, Fin.val_last]
      omega
    have hle := hup (u : ℕ) ⟨m - 1, by omega⟩ hnot
    simp only at hle
    omega
  refine ⟨fun u => ⟨blockCount g (u : ℕ), hlt u⟩, fun u => ⟨?_, ?_⟩⟩
  · rcases Nat.eq_zero_or_pos (blockCount g (u : ℕ)) with hc0 | hcpos
    · have h0 : (⟨blockCount g (u : ℕ), hlt u⟩ : Fin m).castSucc = 0 := by
        refine Fin.ext ?_
        simp [hc0]
      rw [h0, hg0]
      simp
    · have hd : blockCount g (u : ℕ) - 1 < m := by
        have := hlt u
        omega
      have hmem : (g (⟨blockCount g (u : ℕ) - 1, hd⟩ : Fin m).succ : ℕ) ≤ (u : ℕ) := by
        by_contra hnot
        have hle := hup (u : ℕ) ⟨blockCount g (u : ℕ) - 1, hd⟩ hnot
        simp only at hle
        omega
      have heq : (⟨blockCount g (u : ℕ) - 1, hd⟩ : Fin m).succ
          = (⟨blockCount g (u : ℕ), hlt u⟩ : Fin m).castSucc := by
        refine Fin.ext ?_
        simp only [Fin.val_succ, Fin.val_castSucc]
        omega
      rwa [heq] at hmem
  · by_contra hnot
    push Not at hnot
    have hmem : (⟨blockCount g (u : ℕ), hlt u⟩ : Fin m) ∈
        (Finset.univ : Finset (Fin m)).filter fun j : Fin m => (g j.succ : ℕ) ≤ (u : ℕ) := by
      simp only [Finset.mem_filter, Finset.mem_univ, true_and]
      exact hnot
    have hsub : ((Finset.univ : Finset (Fin m)).filter fun j : Fin m =>
          (j : ℕ) < blockCount g (u : ℕ) + 1)
        ⊆ (Finset.univ : Finset (Fin m)).filter fun j : Fin m => (g j.succ : ℕ) ≤ (u : ℕ) := by
      intro j hj
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hj ⊢
      exact hdown (u : ℕ) j ⟨blockCount g (u : ℕ), hlt u⟩ (Fin.le_def.mpr (by simp only; omega))
        hnot
    have hcard := Finset.card_le_card hsub
    rw [card_filter_val_lt m (blockCount g (u : ℕ) + 1) (by have := hlt u; omega)] at hcard
    rw [← blockCount] at hcard
    omega

/-! ## SC37, step 2: the run-subdivision covering claim -/

/-- The block partitions of a grid into `k` positive nominal blocks: strictly increasing
grid-index boundaries `0 = b_0 < b_1 < ... < b_k = N`. -/
def blockPartitions (N k : ℕ) : Finset (Fin (k + 1) → Fin (N + 1)) :=
  Finset.univ.filter fun b : Fin (k + 1) → Fin (N + 1) =>
    StrictMono b ∧ b 0 = 0 ∧ b (Fin.last k) = Fin.last N

@[simp] theorem mem_blockPartitions {b : Fin (k + 1) → Fin (N + 1)} :
    b ∈ blockPartitions N k ↔ StrictMono b ∧ b 0 = 0 ∧ b (Fin.last k) = Fin.last N := by
  simp [blockPartitions]

/-- If the nodes of a coarse boundary family all occur among the nodes of a finer one, the
coarse block containing a cell is determined by the fine block containing it. -/
private theorem blockMap_eq_of_refines {m : ℕ} {g : Fin (m + 1) → Fin (N + 1)} (hg : Monotone g)
    {b : Fin (k + 1) → Fin (N + 1)} (hb : StrictMono b)
    (hsub : ∀ t : Fin (m + 1), ∃ t' : Fin (k + 1), g t = b t')
    {βg : Fin N → Fin m}
    (hβg : ∀ u : Fin N, (g (βg u).castSucc : ℕ) ≤ (u : ℕ) ∧ (u : ℕ) < (g (βg u).succ : ℕ))
    {βb : Fin N → Fin k}
    (hβb : ∀ u : Fin N, (b (βb u).castSucc : ℕ) ≤ (u : ℕ) ∧ (u : ℕ) < (b (βb u).succ : ℕ))
    {u u' : Fin N} (h : βb u = βb u') : βg u = βg u' := by
  have key : ∀ v v' : Fin N, βb v = βb v' → βg v < βg v' → False := by
    intro v v' hvv hlt
    obtain ⟨t, ht⟩ := hsub (βg v).succ
    have h1 : (v : ℕ) < (g (βg v).succ : ℕ) := (hβg v).2
    have h2 : (g (βg v).succ : ℕ) ≤ (v' : ℕ) := by
      have hstep : g (βg v).succ ≤ g (βg v').castSucc := by
        refine hg (Fin.le_def.mpr ?_)
        have := Fin.lt_def.mp hlt
        simp only [Fin.val_succ, Fin.val_castSucc]
        omega
      exact le_trans (Fin.le_def.mp hstep) (hβg v').1
    have hj1 : (b (βb v).castSucc : ℕ) ≤ (v : ℕ) := (hβb v).1
    have hj2 : (v' : ℕ) < (b (βb v).succ : ℕ) := by
      rw [hvv]; exact (hβb v').2
    have hlt1 : b (βb v).castSucc < b t := by
      rw [← ht]; exact Fin.lt_def.mpr (by omega)
    have hlt2 : b t < b (βb v).succ := by
      rw [← ht]; exact Fin.lt_def.mpr (by omega)
    have ha := Fin.lt_def.mp (hb.lt_iff_lt.mp hlt1)
    have hbb := Fin.lt_def.mp (hb.lt_iff_lt.mp hlt2)
    simp only [Fin.val_castSucc, Fin.val_succ] at ha hbb
    omega
  rcases lt_trichotomy (βg u) (βg u') with hlt | heq | hlt
  · exact absurd (key u u' h hlt) (fun hf => hf)
  · exact heq
  · exact absurd (key u' u h.symm hlt) (fun hf => hf)

/-- A grid-index boundary family has at most as many positive-length blocks as the grid has
cells: distinct positive blocks begin at distinct cells. -/
theorem card_positiveBlocks_comp_le {m : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (g : Fin (m + 1) → Fin (N + 1)) (hg : Monotone g) :
    (positiveBlocks (x ∘ g)).card ≤ N := by
  have hpos : ∀ j ∈ positiveBlocks (x ∘ g), g j.castSucc < g j.succ := by
    intro j hj
    rw [mem_positiveBlocks] at hj
    exact hx.strictMono.lt_iff_lt.mp hj
  have hkey : ∀ j ∈ positiveBlocks (x ∘ g), ∀ j' : Fin m, j < j' →
      (g j.castSucc : ℕ) < (g j'.castSucc : ℕ) := by
    intro j hj j' hjj'
    have h1 := Fin.lt_def.mp (hpos j hj)
    have h2 : g j.succ ≤ g j'.castSucc := by
      refine hg (Fin.le_def.mpr ?_)
      have := Fin.lt_def.mp hjj'
      simp only [Fin.val_succ, Fin.val_castSucc]
      omega
    have h3 := Fin.le_def.mp h2
    omega
  refine le_trans (Finset.card_le_card_of_injOn (t := Finset.range N)
    (fun j => (g j.castSucc : ℕ)) ?_ ?_) (le_of_eq (Finset.card_range N))
  · intro j hj
    have h1 := Fin.lt_def.mp (hpos j hj)
    have h2 : (g j.succ : ℕ) ≤ N := Nat.lt_succ_iff.mp (g j.succ).isLt
    change (g j.castSucc : ℕ) ∈ Finset.range N
    exact Finset.mem_range.mpr (by omega)
  · intro j hj j' hj' heq
    rw [Finset.mem_coe] at hj hj'
    rcases lt_trichotomy j j' with h | h | h
    · exact absurd heq (Nat.ne_of_lt (hkey j hj j' h))
    · exact h
    · exact absurd heq.symm (Nat.ne_of_lt (hkey j' hj' j h))

/-- SC37, the first clause of the covering claim: a grid schedule with at most `s` switches
has at most `k = min (s + 1, N)` maximal runs.

"Maximal runs" is `IsReduced` of `Formal.GridSwitching.Model`: every block has positive length
and no two consecutive blocks carry the same mode, so the blocks of a reduced parameterization
with the same occupation are exactly the maximal runs of the schedule. Two bounds combine: the
normalization of `exists_isReduced` never produces more blocks than the original word has
positive-length blocks, which is at most `s + 1`, and positive blocks begin at distinct grid
cells, of which there are `N`. -/
theorem exists_isReduced_gridSchedule {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) {s : ℕ}
    {W : Fin n → ℝ → ℝ} (hW : IsGridSchedule x (s + 1) W) :
    ∃ (r : ℕ) (q : Fin r → Fin n) (σ : Fin (r + 1) → ℝ),
      r ≤ min (s + 1) N ∧ OrderedTimes σ T ∧ IsReduced q σ ∧ occupation q σ = W := by
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := hW
  have hτ : OrderedTimes (x ∘ g) T := orderedTimes_comp_blockMap hx hg hg0 hgl
  obtain ⟨r, q, σ, hσ, hred, hocc, hr⟩ := exists_isReduced p (x ∘ g) hτ
  refine ⟨r, q, σ, ?_, hσ, hred, hocc⟩
  have h1 : (positiveBlocks (x ∘ g)).card ≤ s + 1 := by
    simpa using Finset.card_le_card (Finset.subset_univ (positiveBlocks (x ∘ g)))
  have h2 : (positiveBlocks (x ∘ g)).card ≤ N := card_positiveBlocks_comp_le hx g hg
  omega

/-- SC37, the second clause of the covering claim: a grid schedule with at most `s` switches
is the occupation of a word on exactly `k = min (s + 1, N)` nominal blocks, with strictly
increasing grid-index endpoints `0 = b_0 < ... < b_k = N`.

The statement needs no grid hypothesis, so it asserts strict monotonicity of the *indices*
only; on an actual grid, `IsGrid.cellLength_pos` turns that into positive block length, which
is the source's "positive nominal blocks".

The proof is the run subdivision of `thm:fixed-budget`. The distinct switch nodes of the given
schedule number at most `min (s + 2, N + 1) = k + 1` — the node-counting form of the run bound
`exists_isReduced_gridSchedule` — and they are completed to exactly `k + 1` grid nodes, which
is possible because `k ≤ N`. The resulting blocks refine the original ones, so labelling each
of them by the mode of the original block containing it leaves the control unchanged. -/
theorem exists_blockPartition_of_isGridSchedule (hN : 0 < N) {x : Fin (N + 1) → ℝ} {s : ℕ}
    {W : Fin n → ℝ → ℝ} (hW : IsGridSchedule x (s + 1) W) :
    ∃ b ∈ blockPartitions N (min (s + 1) N), ∃ p : Fin (min (s + 1) N) → Fin n,
      W = occupation p (x ∘ b) := by
  classical
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := hW
  set k : ℕ := min (s + 1) N with hk
  have hkN : k ≤ N := min_le_right _ _
  have hkpos : 0 < k := lt_min (Nat.succ_pos s) hN
  -- the set of nodes used by the given schedule, completed to `k + 1` nodes
  have hcard₀ : ((Finset.univ : Finset (Fin (s + 2))).image g).card ≤ k + 1 := by
    have h1 : ((Finset.univ : Finset (Fin (s + 2))).image g).card ≤ s + 2 := by
      simpa using Finset.card_image_le (s := (Finset.univ : Finset (Fin (s + 2)))) (f := g)
    have h2 : ((Finset.univ : Finset (Fin (s + 2))).image g).card ≤ N + 1 := by
      simpa using Finset.card_le_card (Finset.subset_univ
        ((Finset.univ : Finset (Fin (s + 2))).image g))
    omega
  obtain ⟨C, hC₀, -, hCcard⟩ := Finset.exists_subsuperset_card_eq
    (Finset.subset_univ ((Finset.univ : Finset (Fin (s + 2))).image g)) hcard₀
    (by simpa using Nat.succ_le_succ hkN)
  set b : Fin (k + 1) → Fin (N + 1) := ⇑(C.orderEmbOfFin hCcard) with hbdef
  have hbmono : StrictMono b := (C.orderEmbOfFin hCcard).strictMono
  have hbsurj : ∀ q ∈ C, ∃ t : Fin (k + 1), b t = q := by
    intro q hq
    have hmem : q ∈ Set.range ⇑(C.orderEmbOfFin hCcard) := by
      rw [Finset.range_orderEmbOfFin]
      exact hq
    exact hmem
  have hgC : ∀ t : Fin (s + 2), g t ∈ C :=
    fun t => hC₀ (Finset.mem_image_of_mem g (Finset.mem_univ t))
  have hsub : ∀ t : Fin (s + 2), ∃ t' : Fin (k + 1), g t = b t' := by
    intro t
    obtain ⟨t', ht'⟩ := hbsurj (g t) (hgC t)
    exact ⟨t', ht'.symm⟩
  have hb0 : b 0 = 0 := by
    obtain ⟨t, ht⟩ := hbsurj 0 (by rw [← hg0]; exact hgC 0)
    refine le_antisymm ?_ (Fin.zero_le _)
    rw [← ht]
    exact hbmono.monotone (Fin.zero_le t)
  have hbl : b (Fin.last k) = Fin.last N := by
    obtain ⟨t, ht⟩ := hbsurj (Fin.last N) (by rw [← hgl]; exact hgC (Fin.last (s + 1)))
    refine le_antisymm (Fin.le_last _) ?_
    rw [← ht]
    exact hbmono.monotone (Fin.le_last t)
  -- the two cell-to-block maps
  obtain ⟨βg, hβg⟩ := exists_blockMap hg hg0 hgl
  obtain ⟨βb, hβb⟩ := exists_blockMap hbmono.monotone hb0 hbl
  -- a cell of each new block
  have hcell : ∀ j : Fin k, (b j.castSucc : ℕ) < N := by
    intro j
    have h1 := Fin.lt_def.mp (hbmono (Fin.castSucc_lt_succ (i := j)))
    have h2 : (b j.succ : ℕ) ≤ N := Nat.lt_succ_iff.mp (b j.succ).isLt
    omega
  set firstCell : Fin k → Fin N := fun j => ⟨(b j.castSucc : ℕ), hcell j⟩ with hfc
  have hfirst : ∀ j : Fin k, βb (firstCell j) = j := by
    intro j
    refine block_unique hbmono.monotone (hβb (firstCell j)) ⟨le_rfl, ?_⟩
    exact Fin.lt_def.mp (hbmono (Fin.castSucc_lt_succ (i := j)))
  refine ⟨b, mem_blockPartitions.mpr ⟨hbmono, hb0, hbl⟩, fun j => p (βg (firstCell j)), ?_⟩
  rw [occupation_blockMap x hg p hβg, occupation_blockMap x hbmono.monotone
    (fun j => p (βg (firstCell j))) hβb]
  refine congrArg (fun q => occupation q x) (funext fun u => ?_)
  refine congrArg p (blockMap_eq_of_refines hg hbmono hsub hβg hβb ?_).symm
  rw [hfirst (βb u)]

/-! ## SC37, step 3: the fixed-budget optimum -/

/-- Every word on a block partition into at most `s + 1` blocks is a grid schedule with at
most `s` switches. -/
theorem isGridSchedule_of_mem_blockPartitions (hn : 0 < n) (x : Fin (N + 1) → ℝ) {s : ℕ}
    (hks : k ≤ s + 1) {b : Fin (k + 1) → Fin (N + 1)} (hb : b ∈ blockPartitions N k)
    (p : Fin k → Fin n) : IsGridSchedule x (s + 1) (occupation p (x ∘ b)) := by
  obtain ⟨hbm, hb0, hbl⟩ := mem_blockPartitions.mp hb
  exact IsGridSchedule.mono hn hks ⟨p, b, hbm.monotone, hb0, hbl, rfl⟩

/-- The errors enumerated by the fixed-budget algorithm: one for every choice of `k` nominal
blocks and every assignment of those blocks to modes. -/
def fixedBudgetErrorSet (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ) (k : ℕ) : Set ℝ :=
  {e | ∃ b ∈ blockPartitions N k, ∃ p : Fin k → Fin n, e = D A (occupation p (x ∘ b)) T}

/-- SC37: the exact fixed-budget grid optimum is the least element of the explicitly described
finite family of errors obtained by choosing `k = min (s + 1, N)` nominal blocks and assigning
them to modes. No hypothesis at all is placed on the input `A`, matching the grid asymmetry of
`eq:grid-definitions`. -/
theorem isLeast_gridOPT_fixedBudget (hn : 0 < n) (hN : 0 < N) (x : Fin (N + 1) → ℝ)
    (A : Fin n → ℝ → ℝ) (T : ℝ) (s : ℕ) :
    IsLeast (fixedBudgetErrorSet x A T (min (s + 1) N)) (gridOPT x A T s) := by
  constructor
  · obtain ⟨W, hW, hWeq⟩ := exists_gridOPT_eq hn x A T s
    obtain ⟨b, hb, p, rfl⟩ := exists_blockPartition_of_isGridSchedule hN hW
    exact ⟨b, hb, p, hWeq⟩
  · rintro e ⟨b, hb, p, rfl⟩
    exact csInf_le (gridScheduleErrorSet_finite x A T (s + 1)).bddBelow
      ⟨occupation p (x ∘ b),
        isGridSchedule_of_mem_blockPartitions hn x (min_le_left _ _) hb p, rfl⟩

/-- SC36 and SC37 combined, the content of `thm:fixed-budget`: the exact grid optimum with at
most `s` switches is obtained by running the subset recurrence `eq:subset-DP` on each of the
finitely many partitions of the grid into `k = min (s + 1, N)` nominal blocks and keeping the
best answer.

`ENNReal.ofReal` clamps negative reals to `0`, so the equation would be vacuous for a negative
optimum. The first conjunct records that this does not happen: under these hypotheses
`gridOPT x A T s` is nonnegative, so `ENNReal.ofReal` is injective on it and the equation
determines the optimum. -/
theorem ofReal_gridOPT_eq_iInf_subsetDP (hn : 0 < n) (hN : 0 < N) {x : Fin (N + 1) → ℝ}
    {T : ℝ} (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    0 ≤ gridOPT x A T s ∧
      ENNReal.ofReal (gridOPT x A T s)
        = ⨅ b ∈ blockPartitions N (min (s + 1) N),
            subsetDP (modeCost x b A) n Finset.univ := by
  refine ⟨gridOPT_nonneg hn hx hA hx.horizon_nonneg s, ?_⟩
  obtain ⟨hmem, hlb⟩ := isLeast_gridOPT_fixedBudget hn hN x A T s
  have hdp : ∀ b ∈ blockPartitions N (min (s + 1) N),
      subsetDP (modeCost x b A) n Finset.univ
        = ⨅ p : Fin (min (s + 1) N) → Fin n, ENNReal.ofReal (D A (occupation p (x ∘ b)) T) := by
    intro b hb
    obtain ⟨hbm, hb0, hbl⟩ := mem_blockPartitions.mp hb
    exact subsetDP_eq_iInf_D hn hx hbm.monotone hb0 hbl hA
  refine le_antisymm (le_iInf fun b => le_iInf fun hb => ?_) ?_
  · rw [hdp b hb]
    exact le_iInf fun p => ENNReal.ofReal_le_ofReal (hlb ⟨b, hb, p, rfl⟩)
  · obtain ⟨b, hb, p, hp⟩ := hmem
    refine le_trans (iInf_le_of_le b (iInf_le_of_le hb le_rfl)) ?_
    rw [hdp b hb, hp]
    exact iInf_le _ p

/-! ## SC37, step 4: the size recursions

`CLAIMS.md` excludes *machine-level bit-complexity* claims only, and records that the verified
content of an algorithmic claim is its correctness, termination and exact arithmetic-operation
or size recursions. Accordingly this section proves the exact sizes of the objects the source's
bounds are sums over, and claims nothing about bit lengths, machine words or running time.

* `card_subsetDP_states`: one mode's layer of `subsetDP` has exactly `2 ^ k` states, the count
  behind the `k 2^k` term of `prop:subset-DP` and behind its `O(n 2^k)` storage.
* `card_subsetDP_transitions`: that layer has exactly `3 ^ k` state-transition pairs, since
  `subsetDP_succ` minimizes over `U ∈ S.powerset` at the state `S`. This is the source's
  `∑_{S ⊆ [k]} 2^{|S|} = 3^k`.
* `subsetDPStates`, `subsetDPTransitions`, `card_subsetDPStates`, `card_subsetDPTransitions`:
  the same two counts stated about the DP's own objects. `subsetDP_succ_eq_inf_transitions`
  shows that `subsetDPTransitions` is the literal index set of the recurrence at a state, and
  `subsetDPTransitions_target` that a transition leads to a state of the previous layer.
* `card_blockPartitions`: there are exactly `binom (N - 1, k - 1)` block partitions, one for
  each choice of the `k - 1` internal boundaries among the `N - 1` internal grid nodes. This
  is the outer factor of `eq:fixed-budget-complexity`.

What is *not* claimed: no statement below or above converts these counts into a number of
arithmetic operations performed by an execution model, and no bit-cost model appears anywhere
in the module. -/

/-- The number of states of one mode's layer of `subsetDP`. -/
theorem card_subsetDP_states (k : ℕ) :
    ((Finset.univ : Finset (Fin k)).powerset).card = 2 ^ k := by
  rw [Finset.card_powerset, Finset.card_univ, Fintype.card_fin]

/-- The number of state-transition pairs of one mode's layer of `subsetDP`: at the state `S`
the recurrence `subsetDP_succ` ranges over `U ∈ S.powerset`, and
`∑_{S ⊆ [k]} 2 ^ |S| = 3 ^ k`. -/
theorem card_subsetDP_transitions (k : ℕ) :
    ∑ S ∈ (Finset.univ : Finset (Fin k)).powerset, S.powerset.card = 3 ^ k := by
  have h := Finset.prod_add (fun _ : Fin k => (2 : ℕ)) (fun _ : Fin k => (1 : ℕ))
    (Finset.univ : Finset (Fin k))
  simp only [Finset.prod_const, Finset.card_univ, Fintype.card_fin, one_pow, mul_one] at h
  simp only [Finset.card_powerset]
  exact h.symm.trans (by norm_num)

/-- The states of one mode's layer of `subsetDP`: the sets of blocks at which the layer is
evaluated. Every argument of `subsetDP c m` is a state, by `mem_subsetDPStates`. -/
def subsetDPStates (k : ℕ) : Finset (Finset (Fin k)) := (Finset.univ : Finset (Fin k)).powerset

@[simp] theorem mem_subsetDPStates {S : Finset (Fin k)} : S ∈ subsetDPStates k :=
  Finset.mem_powerset.mpr (Finset.subset_univ S)

/-- The state-transition pairs of one mode's layer of `subsetDP`: the pairs `⟨S, U⟩` over
which the recurrence `subsetDP_succ` minimizes at the state `S`, namely `U ∈ S.powerset`. The
transition `⟨S, U⟩` assigns the blocks `U` to the current mode and moves to the state `S \ U`
of the previous layer. -/
def subsetDPTransitions (k : ℕ) : Finset ((_ : Finset (Fin k)) × Finset (Fin k)) :=
  (subsetDPStates k).sigma fun S => S.powerset

@[simp] theorem mem_subsetDPTransitions {p : (_ : Finset (Fin k)) × Finset (Fin k)} :
    p ∈ subsetDPTransitions k ↔ p.2 ⊆ p.1 := by
  simp [subsetDPTransitions, Finset.mem_sigma]

/-- A transition of one layer leads from a state of that layer to a state of the previous
layer. -/
theorem subsetDPTransitions_target {p : (_ : Finset (Fin k)) × Finset (Fin k)}
    (_ : p ∈ subsetDPTransitions k) : p.1 ∈ subsetDPStates k ∧ p.1 \ p.2 ∈ subsetDPStates k :=
  ⟨mem_subsetDPStates, mem_subsetDPStates⟩

/-- The recurrence `eq:subset-DP` minimizes over exactly the transitions out of the state `S`:
`subsetDPTransitions` is the literal index set of `subsetDP_succ`. -/
theorem subsetDP_succ_eq_inf_transitions (c : ℕ → Finset (Fin k) → ℝ≥0∞) (m : ℕ)
    (S : Finset (Fin k)) :
    subsetDP c (m + 1) S =
      ((subsetDPTransitions k).filter
          fun p : (_ : Finset (Fin k)) × Finset (Fin k) => p.1 = S).inf
        fun p => c m p.2 ⊔ subsetDP c m (p.1 \ p.2) := by
  rw [subsetDP_succ]
  refine le_antisymm (Finset.le_inf fun p hp => ?_) (Finset.le_inf fun U hU => ?_)
  · obtain ⟨hmem, hfst⟩ := Finset.mem_filter.mp hp
    have hsub : p.2 ⊆ S := hfst ▸ mem_subsetDPTransitions.mp hmem
    have := Finset.inf_le (f := fun U => c m U ⊔ subsetDP c m (S \ U))
      (Finset.mem_powerset.mpr hsub)
    rwa [hfst]
  · have hmem : (⟨S, U⟩ : (_ : Finset (Fin k)) × Finset (Fin k)) ∈
        (subsetDPTransitions k).filter
          fun p : (_ : Finset (Fin k)) × Finset (Fin k) => p.1 = S :=
      Finset.mem_filter.mpr ⟨mem_subsetDPTransitions.mpr (Finset.mem_powerset.mp hU), rfl⟩
    exact Finset.inf_le hmem

/-- SC37, the exact number of states of one mode's layer of `subsetDP`, stated about the
states themselves: there are `2 ^ k` of them. -/
theorem card_subsetDPStates (k : ℕ) : (subsetDPStates k).card = 2 ^ k :=
  card_subsetDP_states k

/-- SC37, the exact number of state-transition pairs of one mode's layer of `subsetDP`,
stated about the transitions themselves: there are `3 ^ k` of them, one for each state `S` and
each `U ∈ S.powerset` examined by `subsetDP_succ`. -/
theorem card_subsetDPTransitions (k : ℕ) : (subsetDPTransitions k).card = 3 ^ k := by
  rw [subsetDPTransitions, Finset.card_sigma]
  exact card_subsetDP_transitions k

/-- SC37, the exact size of the enumeration: the partitions of the grid into `k` nominal
blocks correspond to the choices of `k - 1` internal boundaries among the `N - 1` internal
grid nodes, so there are exactly `binom (N - 1, k - 1)` of them. -/
theorem card_blockPartitions (hN : 0 < N) (hk : 0 < k) :
    (blockPartitions N k).card = (N - 1).choose (k - 1) := by
  classical
  have hzne : (0 : Fin (N + 1)) ≠ Fin.last N := fun h => by
    have hv := congrArg Fin.val h
    simp only [Fin.val_zero, Fin.val_last] at hv
    omega
  set internal : Finset (Fin (N + 1)) :=
    (Finset.univ : Finset (Fin (N + 1))) \ {0, Fin.last N} with hint
  have hpair : ({0, Fin.last N} : Finset (Fin (N + 1))).card = 2 := by
    rw [Finset.card_insert_of_notMem (by simpa using hzne), Finset.card_singleton]
  have hintcard : internal.card = N - 1 := by
    rw [hint, Finset.card_sdiff_of_subset (Finset.subset_univ _), Finset.card_univ,
      Fintype.card_fin, hpair]
    omega
  have hsubpair : ∀ b ∈ blockPartitions N k,
      ({0, Fin.last N} : Finset (Fin (N + 1)))
        ⊆ (Finset.univ : Finset (Fin (k + 1))).image b := by
    intro b hb q hq
    obtain ⟨-, hb0, hbl⟩ := mem_blockPartitions.mp hb
    simp only [Finset.mem_insert, Finset.mem_singleton] at hq
    rcases hq with rfl | rfl
    · exact Finset.mem_image.mpr ⟨0, Finset.mem_univ _, hb0⟩
    · exact Finset.mem_image.mpr ⟨Fin.last k, Finset.mem_univ _, hbl⟩
  have himg : ∀ b ∈ blockPartitions N k,
      ((Finset.univ : Finset (Fin (k + 1))).image b).card = k + 1 := by
    intro b hb
    obtain ⟨hbm, -, -⟩ := mem_blockPartitions.mp hb
    rw [Finset.card_image_of_injective _ hbm.injective, Finset.card_univ, Fintype.card_fin]
  rw [← hintcard, ← Finset.card_powersetCard]
  refine Finset.card_nbij
    (fun b => ((Finset.univ : Finset (Fin (k + 1))).image b) \ {0, Fin.last N}) ?_ ?_ ?_
  · intro b hb
    rw [Finset.mem_coe] at hb
    refine Finset.mem_coe.mpr (Finset.mem_powersetCard.mpr ⟨fun q hq => ?_, ?_⟩)
    · rw [Finset.mem_sdiff] at hq ⊢
      exact ⟨Finset.mem_univ q, hq.2⟩
    · rw [Finset.card_sdiff_of_subset (hsubpair b hb), himg b hb, hpair]
      omega
  · intro b hb b' hb' heq
    rw [Finset.mem_coe] at hb hb'
    have heq' : ((Finset.univ : Finset (Fin (k + 1))).image b) \ {0, Fin.last N}
        = ((Finset.univ : Finset (Fin (k + 1))).image b') \ {0, Fin.last N} := heq
    have himgeq : (Finset.univ : Finset (Fin (k + 1))).image b
        = (Finset.univ : Finset (Fin (k + 1))).image b' := by
      rw [← Finset.sdiff_union_of_subset (hsubpair b hb),
        ← Finset.sdiff_union_of_subset (hsubpair b' hb'), heq']
    obtain ⟨hbm, -, -⟩ := mem_blockPartitions.mp hb
    obtain ⟨hb'm, -, -⟩ := mem_blockPartitions.mp hb'
    have hmemb' : ∀ t : Fin (k + 1), b' t ∈ (Finset.univ : Finset (Fin (k + 1))).image b := by
      intro t
      rw [himgeq]
      exact Finset.mem_image_of_mem b' (Finset.mem_univ t)
    have h1 : b = ((Finset.univ : Finset (Fin (k + 1))).image b).orderEmbOfFin (himg b hb) :=
      Finset.orderEmbOfFin_unique (himg b hb)
        (fun t => Finset.mem_image_of_mem b (Finset.mem_univ t)) hbm
    have h2 : b' = ((Finset.univ : Finset (Fin (k + 1))).image b).orderEmbOfFin (himg b hb) :=
      Finset.orderEmbOfFin_unique (himg b hb) hmemb' hb'm
    exact h1.trans h2.symm
  · intro C' hC'
    rw [Finset.mem_coe, Finset.mem_powersetCard] at hC'
    obtain ⟨hCsub, hCcard'⟩ := hC'
    have h0C' : (0 : Fin (N + 1)) ∉ C' := by
      intro hmem
      have := hCsub hmem
      rw [hint, Finset.mem_sdiff] at this
      exact this.2 (by simp)
    have hlC' : (Fin.last N : Fin (N + 1)) ∉ C' := by
      intro hmem
      have := hCsub hmem
      rw [hint, Finset.mem_sdiff] at this
      exact this.2 (by simp)
    set C : Finset (Fin (N + 1)) := insert 0 (insert (Fin.last N) C') with hCdef
    have hnot0 : (0 : Fin (N + 1)) ∉ insert (Fin.last N) C' := by
      simp only [Finset.mem_insert]
      exact fun hc => hc.elim hzne h0C'
    have hCcard : C.card = k + 1 := by
      rw [hCdef, Finset.card_insert_of_notMem hnot0, Finset.card_insert_of_notMem hlC',
        hCcard']
      omega
    set b : Fin (k + 1) → Fin (N + 1) := ⇑(C.orderEmbOfFin hCcard) with hbdef
    have hbmono : StrictMono b := (C.orderEmbOfFin hCcard).strictMono
    have hbimage : (Finset.univ : Finset (Fin (k + 1))).image b = C :=
      Finset.image_orderEmbOfFin_univ C hCcard
    have hbsurj : ∀ q ∈ C, ∃ t : Fin (k + 1), b t = q := by
      intro q hq
      have hmem : q ∈ Set.range ⇑(C.orderEmbOfFin hCcard) := by
        rw [Finset.range_orderEmbOfFin]
        exact hq
      exact hmem
    have hb0 : b 0 = 0 := by
      obtain ⟨t, ht⟩ := hbsurj 0 (by rw [hCdef]; exact Finset.mem_insert_self _ _)
      refine le_antisymm ?_ (Fin.zero_le _)
      rw [← ht]
      exact hbmono.monotone (Fin.zero_le t)
    have hbl : b (Fin.last k) = Fin.last N := by
      obtain ⟨t, ht⟩ := hbsurj (Fin.last N) (by
        rw [hCdef]
        exact Finset.mem_insert_of_mem (Finset.mem_insert_self _ _))
      refine le_antisymm (Fin.le_last _) ?_
      rw [← ht]
      exact hbmono.monotone (Fin.le_last t)
    refine ⟨b, Finset.mem_coe.mpr (mem_blockPartitions.mpr ⟨hbmono, hb0, hbl⟩), ?_⟩
    change ((Finset.univ : Finset (Fin (k + 1))).image b) \ {0, Fin.last N} = C'
    rw [hbimage, hCdef]
    ext q
    simp only [Finset.mem_sdiff, Finset.mem_insert, Finset.mem_singleton]
    constructor
    · rintro ⟨h1 | h1 | h1, h2⟩
      · exact absurd (Or.inl h1) h2
      · exact absurd (Or.inr h1) h2
      · exact h1
    · intro h
      refine ⟨Or.inr (Or.inr h), ?_⟩
      rintro (rfl | rfl)
      · exact h0C' h
      · exact hlC' h

/-- SC37, the enumeration bound, the form used by `eq:fixed-budget-complexity`. -/
theorem card_blockPartitions_le (hN : 0 < N) (hk : 0 < k) :
    (blockPartitions N k).card ≤ (N - 1).choose (k - 1) :=
  le_of_eq (card_blockPartitions hN hk)

end GridSwitching
