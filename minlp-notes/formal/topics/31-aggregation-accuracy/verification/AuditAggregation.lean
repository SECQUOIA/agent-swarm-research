import Formal.InfiniteAggregation.Accuracy
import Formal.InfiniteAggregation.AccuracyAngular
import Formal.InfiniteAggregation.AccuracyConstants
import Formal.InfiniteAggregation.AccuracyLower
import Formal.InfiniteAggregation.AccuracyLowerGap
import Formal.InfiniteAggregation.AccuracyLowerLipschitz
import Formal.InfiniteAggregation.AccuracyLowerPigeonhole
import Formal.InfiniteAggregation.AccuracyMesh
import Formal.InfiniteAggregation.AccuracyModel
import Formal.InfiniteAggregation.AccuracyRate
import Formal.InfiniteAggregation.AccuracyRational
import Formal.InfiniteAggregation.AccuracyRationalBound
import Formal.InfiniteAggregation.AccuracyRationalMesh
import Formal.InfiniteAggregation.AccuracyUpper
import Formal.InfiniteAggregation.AccuracyUpperGeometry
import Lean.Util.CollectAxioms

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.InfiniteAggregation.Accuracy,
    `Formal.InfiniteAggregation.AccuracyAngular,
    `Formal.InfiniteAggregation.AccuracyConstants,
    `Formal.InfiniteAggregation.AccuracyLower,
    `Formal.InfiniteAggregation.AccuracyLowerGap,
    `Formal.InfiniteAggregation.AccuracyLowerLipschitz,
    `Formal.InfiniteAggregation.AccuracyLowerPigeonhole,
    `Formal.InfiniteAggregation.AccuracyMesh,
    `Formal.InfiniteAggregation.AccuracyModel,
    `Formal.InfiniteAggregation.AccuracyRate,
    `Formal.InfiniteAggregation.AccuracyRational,
    `Formal.InfiniteAggregation.AccuracyRationalBound,
    `Formal.InfiniteAggregation.AccuracyRationalMesh,
    `Formal.InfiniteAggregation.AccuracyUpper,
    `Formal.InfiniteAggregation.AccuracyUpperGeometry]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-31 declarations across {owners.size} modules."
