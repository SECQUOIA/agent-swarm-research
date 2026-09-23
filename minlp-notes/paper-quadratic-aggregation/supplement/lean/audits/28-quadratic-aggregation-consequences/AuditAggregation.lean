import Formal.QuadraticAggregation.Boundary
import Formal.QuadraticAggregation.ClosedSystem
import Formal.QuadraticAggregation.Consequences
import Formal.QuadraticAggregation.Dines
import Formal.QuadraticAggregation.SDPCharacterization
import Formal.QuadraticAggregation.ShorAlgebra
import Formal.QuadraticAggregation.ShorBlock
import Formal.QuadraticAggregation.ShorConeSeparation
import Formal.QuadraticAggregation.ShorDuality
import Formal.QuadraticAggregation.ShorModel
import Lean.Util.CollectAxioms

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.QuadraticAggregation.Boundary,
    `Formal.QuadraticAggregation.ClosedSystem,
    `Formal.QuadraticAggregation.Consequences,
    `Formal.QuadraticAggregation.Dines,
    `Formal.QuadraticAggregation.SDPCharacterization,
    `Formal.QuadraticAggregation.ShorAlgebra,
    `Formal.QuadraticAggregation.ShorBlock,
    `Formal.QuadraticAggregation.ShorConeSeparation,
    `Formal.QuadraticAggregation.ShorDuality,
    `Formal.QuadraticAggregation.ShorModel]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-28 declarations across {owners.size} modules."
