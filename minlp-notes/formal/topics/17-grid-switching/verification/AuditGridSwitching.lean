import Formal.GridSwitching.BinaryTransfer
import Formal.GridSwitching.Coarsening
import Formal.GridSwitching.Compactness
import Formal.GridSwitching.Coverage
import Formal.GridSwitching.Cumulative
import Formal.GridSwitching.Dwell
import Formal.GridSwitching.Elimination
import Formal.GridSwitching.Endpoint
import Formal.GridSwitching.Examples
import Formal.GridSwitching.FiniteOne
import Formal.GridSwitching.InstanceAlgorithms
import Formal.GridSwitching.LinearPrograms
import Formal.GridSwitching.Model
import Formal.GridSwitching.OneSwitch
import Formal.GridSwitching.Refinement
import Formal.GridSwitching.Rounding
import Formal.GridSwitching.Sharpness
import Formal.GridSwitching.SubsetDP
import Formal.GridSwitching.Symmetrize
import Formal.GridSwitching.ThreeMode
import Formal.GridSwitching.Transfer
import Formal.GridSwitching.TwoLarge
import Formal.GridSwitching.UniformTransfer
import Lean.Util.CollectAxioms
/-! ## Declarations added when audit findings were closed

The sweep below already covers these, since it ranges over every declaration the
`GridSwitching` modules own. They are named here so the artifact records exactly
what was added when the coverage map's overstatements were corrected: the
one-switch refinement generalized to arbitrary grids, deletion at an arbitrary
position, the size recursions tied to the dynamic program, and the two witnesses
that were previously only docstring calculations. -/

-- SC30: the one-switch refinement, now on an arbitrary grid
#print axioms GridSwitching.exists_cell_mem_Icc
#print axioms GridSwitching.exists_node_abs_sub_le_meshWidth
#print axioms GridSwitching.gridOPT_le_OPT_add_half_one_switch
#print axioms GridSwitching.coarsening_certificate_one_switch
#print axioms GridSwitching.gridOPT_le_OPT_add_half_one_switch_uniform
#print axioms GridSwitching.coarsening_certificate_one_switch_uniform

-- SC03: deletion at an arbitrary position
#print axioms GridSwitching.occupation_delete_at

-- SC36: the size recursions, tied to the dynamic program
#print axioms GridSwitching.subsetDP_succ_eq_inf_transitions
#print axioms GridSwitching.subsetDPTransitions_target
#print axioms GridSwitching.card_subsetDPStates
#print axioms GridSwitching.card_subsetDPTransitions

-- SC23: the binding discarded term, previously only in a docstring
#print axioms GridSwitching.Examples.nonuniform_binding_discarded_term

-- SC35: the endpoint witness, previously only in a docstring
#print axioms GridSwitching.endpointWitness_lt_D_completion

-- SC24: the negative control -- support feasibility does not imply the prefix bounds
#print axioms GridSwitching.exists_supported_not_prefix_bounded

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => (`Formal.GridSwitching).isPrefixOf mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} GridSwitching declarations."
