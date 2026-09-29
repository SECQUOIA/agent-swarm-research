import Formal.CompetitiveBranching.Model
import Formal.CompetitiveBranching.Lemmas
import Formal.CompetitiveBranching.Counting
import Formal.CompetitiveBranching.Theorem1
import Formal.CompetitiveBranching.Competitive
import Formal.CompetitiveBranching.Pruning
import Lean.Util.CollectAxioms

/-! Audit every declaration owned by the six topic-33 modules, including
private and auxiliary declarations. Fail on any axiom other than `propext`,
`Classical.choice` and `Quot.sound` (in particular on `sorryAx`). -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.CompetitiveBranching.Model,
    `Formal.CompetitiveBranching.Lemmas,
    `Formal.CompetitiveBranching.Counting,
    `Formal.CompetitiveBranching.Theorem1,
    `Formal.CompetitiveBranching.Competitive,
    `Formal.CompetitiveBranching.Pruning]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-33 declarations across {owners.size} modules."

#check @CompetitiveBranching.internal_le
#check @CompetitiveBranching.size_le
#check @CompetitiveBranching.theorem1
#check @CompetitiveBranching.size_lt_four_mul
#print axioms CompetitiveBranching.internal_le
#print axioms CompetitiveBranching.size_le
#print axioms CompetitiveBranching.count_interval_le_three
#print axioms CompetitiveBranching.count_first_interval_le_one
#print axioms CompetitiveBranching.count_last_interval_le_one
#print axioms CompetitiveBranching.count_breakpoint_le_one
#print axioms CompetitiveBranching.eq_leaf_of_certificate_one
#print axioms CompetitiveBranching.key_left
#print axioms CompetitiveBranching.key_right
#print axioms CompetitiveBranching.size_add_three_le
#print axioms CompetitiveBranching.size_lt_four_mul
#print axioms CompetitiveBranching.theorem1
