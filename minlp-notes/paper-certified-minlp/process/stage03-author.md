# Stage 3 author record: focused Lean formalization

Stage author: `/root/formal_author`. This is the author handoff, not stage
acceptance. The coordinator must next dispatch five independent reviewers.

## Delivered work

Created the standalone `formal/` project under this paper. It imports no proof
module from the repository's existing root formalization and changes no root
formal source, CI file, checker code, historical evidence or benchmark run.
The project pins Lean 4.33.1 and mathlib 4.33.1 with a complete dependency
manifest. Development reuses only the ignored dependency cache through a
symlink. The submitted source needs no sibling project.

- `CertifiedMinlp/Coordinates.lean` defines rational finite/one-sided/free
  coordinates and proves the actual rational-enclosure correction inequalities
  in the soundness section's table. Infinite endpoints are constructors. Fixed
  coordinates have zero correction; accepted corrections are nonnegative.
- `CertifiedMinlp/SafeCuts.lean` proves finite-sum support correction and its
  rational-enclosure specialization. The actual real residual slopes are
  enclosed by rational endpoints; the conclusion is the affine underestimator.
  The final inequality is not assumed. The finite coordinate type can be empty.
- `CertifiedMinlp/Transfer.lean` proves objective-preserving lower-bound and
  infeasibility transfer, graph-feasible epigraph construction and bound
  transfer, epigraph-cut validity from underestimation, objective signs,
  weak-incumbent-cutoff lifting, primal-gap bounds, matching-witness attainment,
  and real-infimum bounds after proving nonemptiness and boundedness below.
- `Verify.lean` audits every project-owned declaration including generated and
  private declarations, rejecting any transitive axiom except `propext`,
  `Classical.choice`, `Quot.sound`. The verification script also checks complete
  import coverage, builds with warnings as failures, and replays compiled
  project declarations with `leanchecker` and one worker.
- `formal/COVERAGE.md` maps assertions to theorem names and premises. It lists
  exclusions rather than treating mathematical implications as executable
  verification.
- `sections/05-formalization.tex` explains these results, their representations,
  proof mechanisms, and limitations. The introduction's conditional sentence
  was replaced by the actual proved coverage and a section reference.

## Mathematical scope decisions

The source support inequality and actual value/gradient enclosure inequalities
remain premises. Deriving supports from convexity/domain/differentiability and
computing actual interval enclosures are excluded. No arbitrary final safe-cut
inequality is hidden as a premise of `rational_enclosure_cut`.

The coordinate proofs establish all sufficient table inequalities for accepted
cuts. They do not mechanize supremum notation or necessity of the finite-sign
conditions. The distinction is explicit in both manuscript and coverage.

Generic transfer assumes feasible embedding and objective equality, which are
exactly the unmechanized master-interface obligations. The epigraph theorem
also constructs its particular embedding from a base-set inclusion and cut
validity. The cutoff theorem assumes the derived bound on the restricted set;
it proves the nontrivial extension through the checked incumbent, rather than
claiming the VIPR inference invariant or executable kernel is formalized.

The infimum theorem assumes an actual feasible witness and a finite global
lower bound, then proves the conditions needed for the real conditional
infimum. Empty feasible sets are covered by pointwise transfer, without
incorrectly interpreting the real `sInf` of the empty set as positive infinity.

## Validation

`formal/verification/run.log` records the local build, audit and kernel replay:
three proof modules, 95 audited project declarations, all checks pass. The
main theorem axiom lists contain only the three allowed standard axioms. The
first build exposed one unused `Fintype` section parameter in the row-validity
lemma; it was removed before the successful warning-free verification.

`formal/verification/isolated-run.log` records an additional source-copy build
outside the repository with no preexisting project build products. The exact
same cached pinned dependencies are reused; no root project proof module is
imported. This tests source independence while avoiding a redundant network
download. It does not claim a fresh recompilation or kernel replay of all
mathlib dependencies. The transient build path is recorded separately in
`process/stage03-isolated-path.txt`.

The actual mathlib checkout reports commit
`0df444a360eaa60ab8c11dca51a86af692955474`, matching the manifest. Source
fingerprints are in `formal/verification/SHA256SUMS`. Run
`sha256sum -c verification/SHA256SUMS` from the formal directory to check them.

The current complete paper compiles via
`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`.
The build command output is `build/stage03-latex.log`; the final LaTeX log
contains no warning, undefined-reference, or overfull/underfull-box messages.
No numerical experiment or benchmark recheck was run during this stage.
