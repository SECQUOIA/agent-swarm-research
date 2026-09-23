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

#print axioms MultilinearGap.unbounded_gap_ratio
#print axioms MultilinearGap.no_uniform_positive_multilinear_bound
#print axioms MultilinearGap.termwiseGap_eq
#print axioms MultilinearGap.hullGap_exact_upper_bound
#print axioms MultilinearGap.exists_exact_attaining_law
#print axioms MultilinearGap.exists_hullGap_exact
#print axioms MultilinearGap.sharp_cube_gap_bound
#print axioms MultilinearGap.degree_gap_bound_on_box
#print axioms MultilinearGap.sharp_positive_growth
#print axioms MultilinearGap.monomial_minimum
#print axioms MultilinearGap.box_convex_envelope
#print axioms MultilinearGap.box_concave_envelope
#print axioms MultilinearGap.box_gap_comparison
#print axioms MultilinearGap.boxTermwiseGap_eq_term_gaps
#print axioms MultilinearGap.supports_card
#print axioms MultilinearGap.supports_max_degree
#print axioms MultilinearGap.supports_occurrences
#print axioms MultilinearGap.supports_occurrences_isBigO
#print axioms MultilinearGap.tendsto_exact_family_ratio_normalized
#print axioms MultilinearGap.example_sixty_four
