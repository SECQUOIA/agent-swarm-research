import Formal.PotentialFlow.Bregman
import Formal.PotentialFlow.Bisection
import Formal.PotentialFlow.Curvature
import Formal.PotentialFlow.DyadicRoot
import Formal.PotentialFlow.FieldDuality
import Formal.PotentialFlow.Laplacian
import Formal.PotentialFlow.Scenario
import Formal.PotentialFlow.Support
import Formal.PotentialFlow.SupportComplete
import Formal.PotentialFlow.TwoPath
import Formal.PotentialFlow.TwoPathComparison
import Formal.PotentialFlow.CertResults
import Lean.Util.CollectAxioms

/-! Targeted audit: every declaration owned by a `Formal.PotentialFlow` module. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => (`Formal.PotentialFlow).isPrefixOf mod.module
    return if owned then names.push name else names
  if names.isEmpty then
    throwError "No potential-flow declarations were found; the audit would be empty."
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    let axioms ← Lean.collectAxioms name
    for axiomName in axioms do
      unless allowed.contains axiomName do
        throwError "{name} depends on disallowed axiom {axiomName}"
  logInfo m!"PASS: audited {names.size} potential-flow declarations."
