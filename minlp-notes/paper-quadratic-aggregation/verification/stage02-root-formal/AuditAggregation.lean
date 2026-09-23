import Formal.QuadraticAggregation.Coefficients
import Formal.QuadraticAggregation.ConeClosed
import Formal.QuadraticAggregation.ConeGeometry
import Formal.QuadraticAggregation.DefinitionsSequence
import Formal.QuadraticAggregation.EasyDirection
import Formal.QuadraticAggregation.Headline
import Formal.QuadraticAggregation.Hyperplanes
import Formal.QuadraticAggregation.LimitCompactness
import Formal.QuadraticAggregation.Model
import Formal.QuadraticAggregation.Recession
import Formal.QuadraticAggregation.SweepBounds
import Lean.Util.CollectAxioms

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.QuadraticAggregation.Coefficients,
    `Formal.QuadraticAggregation.ConeClosed,
    `Formal.QuadraticAggregation.ConeGeometry,
    `Formal.QuadraticAggregation.DefinitionsSequence,
    `Formal.QuadraticAggregation.EasyDirection,
    `Formal.QuadraticAggregation.Headline,
    `Formal.QuadraticAggregation.Hyperplanes,
    `Formal.QuadraticAggregation.LimitCompactness,
    `Formal.QuadraticAggregation.Model,
    `Formal.QuadraticAggregation.Recession,
    `Formal.QuadraticAggregation.SweepBounds]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-27 declarations across {owners.size} modules."
