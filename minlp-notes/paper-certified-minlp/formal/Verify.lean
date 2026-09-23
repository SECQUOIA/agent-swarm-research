import CertifiedMinlp
import Lean.Util.CollectAxioms

/-! Audit every declaration owned by a project module, including private
definitions and auxiliary declarations. Fail on any nonstandard dependency.
Module ownership avoids silently omitting a newly added topic namespace. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => (`CertifiedMinlp).isPrefixOf mod.module
    return if owned then names.push name else names
  if names.isEmpty then
    throwError "No project declarations were found; the audit would be empty."
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    let axioms ← Lean.collectAxioms name
    for axiomName in axioms do
      unless allowed.contains axiomName do
        throwError "{name} depends on disallowed axiom {axiomName}"
  logInfo m!"PASS: audited {names.size} project declarations; \
    only propext, Classical.choice, Quot.sound are allowed."


#print axioms CertifiedMinlp.rational_enclosure_cut
#print axioms CertifiedMinlp.epigraph_bound_transfer
#print axioms CertifiedMinlp.incumbent_cutoff_lifting
#print axioms CertifiedMinlp.primal_infimum_bounds
