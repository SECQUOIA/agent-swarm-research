import Formal.InfiniteAggregation.Cardinality
import Formal.InfiniteAggregation.ClosedObstruction
import Formal.InfiniteAggregation.Consequences
import Formal.InfiniteAggregation.Good
import Formal.InfiniteAggregation.GoodBlock
import Formal.InfiniteAggregation.GoodConvex
import Formal.InfiniteAggregation.GoodMatrix
import Formal.InfiniteAggregation.GoodSpectral
import Formal.InfiniteAggregation.GramBound
import Formal.InfiniteAggregation.GramConcavity
import Formal.InfiniteAggregation.GramFrame
import Formal.InfiniteAggregation.GramSupport
import Formal.InfiniteAggregation.Hyperplane
import Formal.InfiniteAggregation.HyperplaneConvexity
import Formal.InfiniteAggregation.Inertia
import Formal.InfiniteAggregation.Model
import Formal.InfiniteAggregation.Rays
import Formal.InfiniteAggregation.Witness
import Lean.Util.CollectAxioms

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.InfiniteAggregation.Cardinality,
    `Formal.InfiniteAggregation.ClosedObstruction,
    `Formal.InfiniteAggregation.Consequences,
    `Formal.InfiniteAggregation.Good,
    `Formal.InfiniteAggregation.GoodBlock,
    `Formal.InfiniteAggregation.GoodConvex,
    `Formal.InfiniteAggregation.GoodMatrix,
    `Formal.InfiniteAggregation.GoodSpectral,
    `Formal.InfiniteAggregation.GramBound,
    `Formal.InfiniteAggregation.GramConcavity,
    `Formal.InfiniteAggregation.GramFrame,
    `Formal.InfiniteAggregation.GramSupport,
    `Formal.InfiniteAggregation.Hyperplane,
    `Formal.InfiniteAggregation.HyperplaneConvexity,
    `Formal.InfiniteAggregation.Inertia,
    `Formal.InfiniteAggregation.Model,
    `Formal.InfiniteAggregation.Rays,
    `Formal.InfiniteAggregation.Witness]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-29 declarations across {owners.size} modules."
