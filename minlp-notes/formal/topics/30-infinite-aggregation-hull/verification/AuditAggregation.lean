import Formal.InfiniteAggregation.Hull
import Formal.InfiniteAggregation.HullClosedConsequences
import Formal.InfiniteAggregation.HullClosure
import Formal.InfiniteAggregation.HullCone
import Formal.InfiniteAggregation.HullCore
import Formal.InfiniteAggregation.HullCoreRoots
import Formal.InfiniteAggregation.HullModel
import Formal.InfiniteAggregation.HullRepresentations
import Formal.InfiniteAggregation.Lift
import Formal.InfiniteAggregation.LiftSmall
import Lean.Util.CollectAxioms

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.InfiniteAggregation.Hull,
    `Formal.InfiniteAggregation.HullClosedConsequences,
    `Formal.InfiniteAggregation.HullClosure,
    `Formal.InfiniteAggregation.HullCone,
    `Formal.InfiniteAggregation.HullCore,
    `Formal.InfiniteAggregation.HullCoreRoots,
    `Formal.InfiniteAggregation.HullModel,
    `Formal.InfiniteAggregation.HullRepresentations,
    `Formal.InfiniteAggregation.Lift,
    `Formal.InfiniteAggregation.LiftSmall]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-30 declarations across {owners.size} modules."
