import Formal.DAGSpectral.TopologicalSort

namespace DAGSpectral
variable {v m : ℕ}

/-- Scan every listed edge, counting the actual incoming-edge tests.
Membership tests on the remaining finite set are part of each edge test. -/
def incomingScan (src dst : Fin m → Fin v) (remaining : Finset (Fin v)) (x : Fin v) :
    List (Fin m) → Bool × ℕ
  | [] => (true,0)
  | e :: es =>
    let tail := incomingScan src dst remaining x es
    (decide (dst e = x → src e ∉ remaining) && tail.1, tail.2 + 1)

theorem incomingScan_spec (src dst : Fin m → Fin v) (remaining : Finset (Fin v))
    (x : Fin v) (es : List (Fin m)) : incomingScan src dst remaining x es =
      (decide (∀ e ∈ es, dst e = x → src e ∉ remaining), es.length) := by
  induction es with
  | nil => simp [incomingScan]
  | cons e es ih => simp [incomingScan, ih]

/-- A full scan over the explicit vertex and edge arrays; the list records
all tests before selection, so its cost does not hide an ordering oracle. -/
def readyVerticesCounted (src dst : Fin m → Fin v) (remaining : Finset (Fin v)) :
    Finset (Fin v) × ℕ :=
  let tests := (List.finRange v).map
    (fun x => (x, incomingScan src dst remaining x (List.finRange m)))
  (((tests.filter (fun item => decide (item.1 ∈ remaining) && item.2.1)).map Prod.fst).toFinset,
    (tests.map (fun item => item.2.2)).sum)

theorem readyVerticesCounted_spec (src dst : Fin m → Fin v) (remaining : Finset (Fin v)) :
    readyVerticesCounted src dst remaining = (readyVertices src dst remaining, v*m) := by
  apply Prod.ext
  · ext x
    simp [readyVerticesCounted, incomingScan_spec, readyVertices,
      List.mem_map, List.mem_filter, and_assoc]
  · simp [readyVerticesCounted, incomingScan_spec,
      List.finRange, List.sum_ofFn]

/-- Kahn's algorithm with the actual full-scan incoming-edge-test count. -/
def kahnOrderCounted (src dst : Fin m → Fin v) :
    ℕ → Finset (Fin v) → List (Fin v) × ℕ
  | 0, _ => ([],0)
  | n+1, remaining =>
    let ready := readyVerticesCounted src dst remaining
    if h : ready.1.Nonempty then
      let x := ready.1.min' h
      let tail := kahnOrderCounted src dst n (remaining.erase x)
      (x :: tail.1, ready.2 + tail.2)
    else ([],ready.2)

theorem kahnOrderCounted_order (src dst : Fin m → Fin v) (n : ℕ)
    (remaining : Finset (Fin v)) :
    (kahnOrderCounted src dst n remaining).1 = kahnOrder src dst n remaining := by
  induction n generalizing remaining with
  | zero => rfl
  | succ n ih =>
    simp only [kahnOrderCounted, readyVerticesCounted_spec, kahnOrder]
    split_ifs <;> simp [ih]

theorem kahnOrderCounted_cost (src dst : Fin m → Fin v) (n : ℕ)
    (remaining : Finset (Fin v)) :
    (kahnOrderCounted src dst n remaining).2 ≤ n * (v*m) := by
  induction n generalizing remaining with
  | zero => simp [kahnOrderCounted]
  | succ n ih =>
    simp only [kahnOrderCounted, readyVerticesCounted_spec]
    split_ifs with hready
    · have h := ih (remaining.erase ((readyVertices src dst remaining).min' hready))
      calc
        _ ≤ v*m + n*(v*m) := Nat.add_le_add_left h (v*m)
        _ = (n+1)*(v*m) := by ring
    · simp only [Nat.add_mul, one_mul]
      exact Nat.le_add_left _ _

/-- At most v²m incoming-edge tests suffice, including the empty graph.
Each test and each finite-set operation has polynomial size in v and m. -/
theorem topologicalSort_scan_bound (src dst : Fin m → Fin v) :
    (kahnOrderCounted src dst v Finset.univ).2 ≤ v ^ 2 * m := by
  simpa only [pow_two, Nat.mul_assoc] using kahnOrderCounted_cost src dst v Finset.univ

end DAGSpectral
