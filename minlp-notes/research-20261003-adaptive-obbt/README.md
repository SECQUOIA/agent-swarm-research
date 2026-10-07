# Adaptive optimization-based bound tightening

The revised [journal manuscript](../paper-adaptive-obbt/README.md) brings this
study together with the September local-rate theory. It contains the complete
proofs and corrected statements; its companion preserves the original evidence
and records corrections to these older reports.

This continuation develops when to start, stop, and reconsider
optimization-based bound tightening (OBBT). It extends the
[September iterated-OBBT study](../research-20260922/iterated-obbt/)
with finite benefit certificates, constrained-case theory, a checked reference
driver, and a prospective test of an additional SCIP propagator.

Read the [integrated report](document/main.pdf), built from
[LaTeX sources](document/main.tex). The [claim map](document/COVERAGE.md)
states each result's assumptions and implementation coverage. The
[completion assessment](CLOSEOUT.md) distinguishes completed work from broader
open questions; [verification](VERIFICATION.md) records the targeted checks.

The 120-run comparison found fewer auxiliary LPs but no additional solves or
demonstrated net speed benefit. Native SCIP remains the recommended default on
this evidence. The exact certificate results stand separately from that
negative computational finding.

## Developed results

- **Finite remaining-benefit certificates.** Feasible witnesses bound the
  improvement in a frozen round. Witnesses feasible in the relaxation rebuilt
  on their coordinate hull can protect that box through every later round of
  the same monotone relaxation family. Cutoff reuse, objective ceilings,
  residual bounds, and invalid reuse cases have explicit contracts.
  [Theory](theory/remaining-benefit.md), [checker](theory/certificates.py).
- **An exact reference driver.** Every endpoint update requires matching
  rational primal and dual proofs. The driver applies only complete verified
  rounds and distinguishes a certified fixed box from an unfinished or
  inconclusive computation. [Implementation](theory/certified_driver.py).
- **Coupled and nonlinear constraints.** Exact parametric LP regions cover
  active-set changes under fixed-matrix assumptions. A feasible-repair theorem
  transfers relaxation error to a width bound; an explicit nonlinear graph
  has a verified contraction factor. Counterexamples delimit extrapolation
  from observed progress. [Theory and examples](theory/constrained-obbt.md).
- **Allocation of solver effort.** Cost accounting, independent-baseline
  scheduling, and counterexamples explain what an enhancement budget can
  guarantee. A width bound alone does not predict search time.
  [Analysis](theory/effort-allocation.md).
- **An integrated solver policy.** Local tightening, incumbent-triggered
  reconsideration, current-round witness screening, and pilot stopping run
  inside SCIP. Proposed bounds use conservative dual corrections.
  [Implementation contract](implementation.md),
  [source](solver/adaptive_obbt.py).

The exact reference driver and the measured SCIP policy implement different
contracts. The SCIP policy does not use protected-box certificates as a
permanent stopping rule, and a numerical SCIP solve is not an exact MINLP
certificate. A protected box limits what the specified tightening operator can
remove; it is not an original feasible inner set or a proposed new search box.

## Evidence and reproduction

The [prospective experiment](experiments/RESULTS.md) compares native SCIP,
additional fixed-order OBBT, and additional adaptive OBBT on twenty models with
two seeds each. Its [frozen protocol](experiments/frozen/PROTOCOL.md), original
public model files, normalized inputs, source snapshots, raw outcomes, and full
logs are retained. Pilot results are separate from comparative evidence.

The [theory review](reviews/theory-review.md) and
[solver and evidence review](reviews/solver-review.md) record defects found,
corrections, independent checks, and limits. These are internal independent
agent reviews, not journal peer review or whole-program formal verification.
The [literature account](literature/related-work.md) and
[primary-source ledger](literature/source-ledger.md) distinguish established
ingredients from this continuation's synthesis. Publication priority is not
claimed from an unsuccessful literature search.

The [program](PROGRAM.md) defines the workstreams. Previous experimental
outcomes and unrelated work in this repository are preserved.
