import CertifiedMinlp.Composition
import CertifiedMinlp.CutCertificate
import CertifiedMinlp.Discrete
import CertifiedMinlp.DiscreteExamples
import CertifiedMinlp.DiscreteRows
import CertifiedMinlp.DiscreteSolutions
import CertifiedMinlp.DomainExamples
import CertifiedMinlp.EndToEnd
import CertifiedMinlp.ExactCorrections
import CertifiedMinlp.Examples
import CertifiedMinlp.IntervalArithmetic
import CertifiedMinlp.LinearFraction
import CertifiedMinlp.MasterIdentity
import CertifiedMinlp.ModelSemantics
import CertifiedMinlp.Monomial
import CertifiedMinlp.MonomialConcave
import CertifiedMinlp.MonomialHessian
import CertifiedMinlp.MonomialMatrix
import CertifiedMinlp.Propagation
import CertifiedMinlp.Quadratic
import CertifiedMinlp.QuadraticChecker
import CertifiedMinlp.QuadraticElimination
import CertifiedMinlp.QuadraticNorm
import CertifiedMinlp.Support
import Lean.Util.CollectAxioms

/-! Audit only the modules added by the Certified MINLP extension.
This is a targeted audit, not a run of project-wide verification. -/
open Lean Elab Command in
run_cmd do
  let selected : Array Name := #[`CertifiedMinlp.Composition,
    `CertifiedMinlp.CutCertificate,
    `CertifiedMinlp.Discrete,
    `CertifiedMinlp.DiscreteExamples,
    `CertifiedMinlp.DiscreteRows,
    `CertifiedMinlp.DiscreteSolutions,
    `CertifiedMinlp.DomainExamples,
    `CertifiedMinlp.EndToEnd,
    `CertifiedMinlp.ExactCorrections,
    `CertifiedMinlp.Examples,
    `CertifiedMinlp.IntervalArithmetic,
    `CertifiedMinlp.LinearFraction,
    `CertifiedMinlp.MasterIdentity,
    `CertifiedMinlp.ModelSemantics,
    `CertifiedMinlp.Monomial,
    `CertifiedMinlp.MonomialConcave,
    `CertifiedMinlp.MonomialHessian,
    `CertifiedMinlp.MonomialMatrix,
    `CertifiedMinlp.Propagation,
    `CertifiedMinlp.Quadratic,
    `CertifiedMinlp.QuadraticChecker,
    `CertifiedMinlp.QuadraticElimination,
    `CertifiedMinlp.QuadraticNorm,
    `CertifiedMinlp.Support]
  let env ← getEnv
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => selected.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "Empty extension audit"
  for name in names do
    for axiomName in ← Lean.collectAxioms name do
      unless #[`propext, `Classical.choice, `Quot.sound].contains axiomName do
        throwError "{name} depends on disallowed axiom {axiomName}"
  logInfo m!"PASS: audited {names.size} declarations in {selected.size} extension modules; \
    only propext, Classical.choice, Quot.sound are allowed."

#print axioms CertifiedMinlp.CertifiedModel.checked_matched_nonlinear_bound
#print axioms CertifiedMinlp.CertifiedModel.checked_affine_bound
#print axioms CertifiedMinlp.Discrete.checked_bound
#print axioms CertifiedMinlp.rational_quadratic_check_iff_convex
