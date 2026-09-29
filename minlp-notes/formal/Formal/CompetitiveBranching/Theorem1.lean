import Formal.CompetitiveBranching.Counting

/-!
# Theorem 1: the relaxation-minimizer rule in one dimension

Let `[L, U]` be the root, `m > 0` on `[L, U]`, `α > 0`, and let
`L = s 0 < ... < s N = U` be a certificate with `N ≥ 2` intervals. Every
minimizer-rule tree on `[L, U]` (including every partial tree of a run) has

* at most three split points in the interior of each certificate interval,
  and at most one in the interior of each end interval;
* at most `4N - 5` internal nodes and at most `8N - 9` nodes.

If `N = 1`, the root is valid and the tree is a single leaf.
-/

open Set

noncomputable section

namespace CompetitiveBranching

variable {m : ℝ → ℝ} {α L U : ℝ} {N : ℕ} {s : ℕ → ℝ}

/-- Charging: if every point of `(l, u)` satisfies some `P i` with `i ∈ I`,
the number of internal nodes is at most the sum of the counts for `P i`. -/
theorem internal_le_sum {ι : Type*} (I : Finset ι) (P : ι → ℝ → Prop) :
    ∀ (t : Tree) (l u : ℝ), MinRule m α l u t → (∀ z ∈ Icc l u, 0 < m z) →
      (∀ y ∈ Ioo l u, ∃ i ∈ I, P i y) → t.internal ≤ ∑ i ∈ I, t.count (P i) := by
  intro t
  induction t with
  | leaf => intros; simp [Tree.internal]
  | node y tl tr ihl ihr =>
    rintro l u ⟨hnv, hy, hmin, htl, htr⟩ hpos hcov
    obtain ⟨-, hly, hyu⟩ := node_facts hpos hnv hy hmin
    have h1 := ihl l y htl (pos_left hpos hy.2)
      (fun z hz => hcov z ⟨hz.1, hz.2.trans hyu⟩)
    have h2 := ihr y u htr (pos_right hpos hy.1)
      (fun z hz => hcov z ⟨hly.trans hz.1, hz.2⟩)
    obtain ⟨i, hi, hPi⟩ := hcov y ⟨hly, hyu⟩
    have hsplit : ∀ j, (Tree.node y tl tr).count (P j) =
        (Tree.node y .leaf .leaf).count (P j) + tl.count (P j) + tr.count (P j) := by
      intro j
      simp [Tree.count]
    have hone : 1 ≤ ∑ j ∈ I, (Tree.node y .leaf .leaf).count (P j) := by
      calc 1 = (Tree.node y .leaf .leaf).count (P i) := by simp [Tree.count, hPi]
        _ ≤ _ := Finset.single_le_sum
          (f := fun j => (Tree.node y .leaf .leaf).count (P j)) (fun j _ => Nat.zero_le _) hi
    simp only [hsplit, Finset.sum_add_distrib, Tree.internal]
    omega

/-- The half-open certificate intervals `[s j, s (j + 1))`, `j < N`, cover
`(L, U)`. Only the endpoint conditions of the certificate are used. -/
theorem IsCertificate.cover (hc : IsCertificate m α L U N s) :
    ∀ y ∈ Ioo L U, ∃ j ∈ Finset.range N, y ∈ Ico (s j) (s (j + 1)) := by
  intro y hy
  have hex : ∃ k, y < s k := ⟨N, hc.finish ▸ hy.2⟩
  have hk0 : Nat.find hex ≠ 0 := by
    intro h0
    have := Nat.find_spec hex
    rw [h0, hc.start] at this
    exact lt_asymm this hy.1
  obtain ⟨j, hj⟩ := Nat.exists_eq_succ_of_ne_zero hk0
  have hkN : Nat.find hex ≤ N := Nat.find_min' hex (hc.finish ▸ hy.2)
  refine ⟨j, Finset.mem_range.mpr (by omega), ?_, ?_⟩
  · exact not_lt.mp (Nat.find_min hex (show j < Nat.find hex by omega))
  · have := Nat.find_spec hex
    rwa [hj] at this

/-- Lemma 1(ii) at the root: each point, in particular each breakpoint, is
the split point of at most one internal node. -/
theorem count_breakpoint_le_one (hpos : ∀ y ∈ Icc L U, 0 < m y) {t : Tree}
    (ht : MinRule m α L U t) (c : ℝ) : t.count (· = c) ≤ 1 :=
  count_eq_le_one c t L U ht hpos

/-- At most three split points lie in the interior of each certificate
interval. -/
theorem count_interval_le_three (hα : 0 < α) (hpos : ∀ y ∈ Icc L U, 0 < m y)
    (hc : IsCertificate m α L U N s) {t : Tree} (ht : MinRule m α L U t)
    {j : ℕ} (hj : j < N) : t.count (· ∈ Ioo (s j) (s (j + 1))) ≤ 3 :=
  count_le_three hα (hc.lt_succ j hj) (hc.valid j hj) t L U ht hpos

/-- At most one split point lies in the interior of the first certificate
interval. -/
theorem count_first_interval_le_one (hα : 0 < α) (hpos : ∀ y ∈ Icc L U, 0 < m y)
    (hc : IsCertificate m α L U N s) (hN : 1 ≤ N) {t : Tree}
    (ht : MinRule m α L U t) : t.count (· ∈ Ioo (s 0) (s 1)) ≤ 1 :=
  count_le_one_of_left_out hα (hc.lt_succ 0 hN) (hc.valid 0 hN) t L U ht hpos
    (by rw [hc.start]; exact fun h => lt_irrefl _ h.1)

/-- At most one split point lies in the interior of the last certificate
interval `[s j, s (j + 1)]`, `j + 1 = N`. -/
theorem count_last_interval_le_one (hα : 0 < α) (hpos : ∀ y ∈ Icc L U, 0 < m y)
    (hc : IsCertificate m α L U N s) {t : Tree} (ht : MinRule m α L U t)
    {j : ℕ} (hj : j + 1 = N) : t.count (· ∈ Ioo (s j) (s (j + 1))) ≤ 1 :=
  count_le_one_of_right_out hα (hc.lt_succ j (by omega)) (hc.valid j (by omega)) t L U ht
    hpos (by rw [hj, hc.finish]; exact fun h => lt_irrefl _ h.2)

/-- **Theorem 1** (internal nodes). With a certificate of `N ≥ 2` intervals,
every minimizer-rule tree on the root `[L, U]` has at most `4N - 5` internal
nodes. -/
theorem internal_le (hα : 0 < α) (hpos : ∀ y ∈ Icc L U, 0 < m y)
    (hc : IsCertificate m α L U N s) (hN : 2 ≤ N) {t : Tree}
    (ht : MinRule m α L U t) : t.internal ≤ 4 * N - 5 := by
  have hsum := internal_le_sum (Finset.range N) (fun j y => y ∈ Ico (s j) (s (j + 1)))
    t L U ht hpos hc.cover
  have hterm : ∀ j, t.count (· ∈ Ico (s j) (s (j + 1))) ≤
      t.count (· = s j) + t.count (· ∈ Ioo (s j) (s (j + 1))) := fun j =>
    Tree.count_le_add (fun y hy => (eq_or_lt_of_le hy.1).imp Eq.symm fun h => ⟨h, hy.2⟩) t
  have hat0 : t.count (· = s 0) = 0 :=
    count_eq_zero_of_forall t L U ht hpos fun y hy h => by
      rw [h, hc.start] at hy
      exact lt_irrefl _ hy.1
  obtain ⟨n, rfl⟩ : ∃ n, N = n + 2 := ⟨N - 2, by omega⟩
  rw [Finset.sum_range_succ, Finset.sum_range_succ'] at hsum
  have hfirst := (hterm 0).trans
    (add_le_add hat0.le (count_first_interval_le_one hα hpos hc (by omega) ht))
  have hlast := (hterm (n + 1)).trans (add_le_add (count_breakpoint_le_one hpos ht _)
    (count_last_interval_le_one hα hpos hc ht (j := n + 1) rfl))
  have hmid : ∑ i ∈ Finset.range n, t.count (· ∈ Ico (s (i + 1)) (s (i + 1 + 1))) ≤
      ∑ _i ∈ Finset.range n, 4 := by
    refine Finset.sum_le_sum fun i hi => (hterm (i + 1)).trans ?_
    have := count_breakpoint_le_one hpos ht (s (i + 1))
    have := count_interval_le_three hα hpos hc ht (j := i + 1)
      (by simp at hi; omega)
    omega
  simp only [Finset.sum_const, Finset.card_range, smul_eq_mul] at hmid
  simp only [zero_add] at hfirst hsum
  omega

/-- **Theorem 1** (all nodes). With a certificate of `N ≥ 2` intervals, every
minimizer-rule tree on `[L, U]` has at most `8N - 9` nodes. -/
theorem size_le (hα : 0 < α) (hpos : ∀ y ∈ Icc L U, 0 < m y)
    (hc : IsCertificate m α L U N s) (hN : 2 ≤ N) {t : Tree}
    (ht : MinRule m α L U t) : t.size ≤ 8 * N - 9 := by
  have := internal_le hα hpos hc hN ht
  rw [Tree.size_eq]
  omega

/-- With `N = 1` the root is valid, so a minimizer-rule tree is a single leaf. -/
theorem eq_leaf_of_certificate_one (hc : IsCertificate m α L U 1 s) {t : Tree}
    (ht : MinRule m α L U t) : t = .leaf := by
  cases t with
  | leaf => rfl
  | node y tl tr =>
    have hv := hc.valid 0 one_pos
    rw [hc.start, zero_add, hc.finish] at hv
    exact absurd hv ht.1

end CompetitiveBranching
