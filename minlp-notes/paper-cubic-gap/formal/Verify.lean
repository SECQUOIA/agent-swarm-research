import Formal
import Lean.Util.CollectAxioms

/-! Audit every bundled declaration, including private helpers, transitively. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => (`Formal).isPrefixOf mod.module
    return if owned then names.push name else names
  if names.isEmpty then
    throwError "No bundled declarations were found; the audit would be empty."
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    let axioms ← Lean.collectAxioms name
    for axiomName in axioms do
      unless allowed.contains axiomName do
        throwError "{name} depends on disallowed axiom {axiomName}"
  logInfo m!"PASS: audited {names.size} bundled declarations; \
    only propext, Classical.choice, Quot.sound are allowed."

#print axioms CubicGap.cubicRoundingLaw_hasMeans
#print axioms CubicGap.cubicRoundingLaw_support_deficiency
#print axioms CubicGap.cubic_box_gap_bound
#print axioms CubicGap.RoundingOptimality.fixed_mixture_optimal_bound
#print axioms CubicGap.RoundingOptimality.fixed_mixture_optimal_weights_unique
#print axioms CubicGap.analytic_binary_expansion
#print axioms CubicGap.analytic_scaled_minimum_lower
#print axioms CubicGap.analytic_finite_ratio_lower
#print axioms CubicGap.analytic_integer_family_witness
#print axioms CubicGap.cubic_boxDegreeSupremum_sandwich
#print axioms CubicGap.RoundingOptimality.optimal_mixture_guarantee
#print axioms CubicGap.analytic_integer_support_witness
#print axioms CubicGap.RoundingOptimality.fixed_mixture_optimum
